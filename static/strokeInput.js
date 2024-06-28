let paths = [];
let simplifiedPaths = [];
let bestFitsSVG = [];
let times = [];
let allFits = [];
let bestFits = [];

// Function to clear the canvas
function clearCanvas() {
  // Remove all paths from the canvas
  paths.forEach(path => path.remove());
  bestFitsSVG.forEach(path => path.remove());
  
  paths = [];
  simplifiedPaths = [];
  bestFitsSVG = [];
  times = [];
  allFits = [];
  bestFits = [];
}

// Function to clear the canvas
function removeLastStroke() {
  if (bestFitsSVG.length == 0) {
    return; // No strokes to remove
  }
  
  // Also remove corresponding best fit SVG if present
  const lastBestFit = bestFitsSVG.pop();
  lastBestFit.parentNode.removeChild(lastBestFit);
  
  simplifiedPaths.pop();
  times.pop();
  allFits.pop();
  bestFits.pop();
}

export {bestFits, clearCanvas, removeLastStroke};

document.addEventListener('DOMContentLoaded', function () {
  // Get the IDs of interactive elements
  const canvas = document.getElementById('canvas');
  
  // Initialize values
  let drawing = false;
  let neighborhood = 3;
  let speedModifier = 0.6;
  let curveModifier = 1.5;
  let errorThreshold = 200;
  
  // Set values for the physical appearance of the strokes
  const strokeWidth = 10;

  // Add eventListeners to recognize the strokes
  canvas.addEventListener('pointerdown', startDrawing);
  canvas.addEventListener('pointermove', draw);
  canvas.addEventListener('pointerup', endDrawing);
  canvas.addEventListener('pointerleave', endDrawing);

  // Create a new path to store the stroke
  function startDrawing(event) {
    drawing = true;

    // Create a new SVG element (a path)
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', `M${event.offsetX},${event.offsetY}`);
    path.setAttribute('stroke', 'black');
    path.setAttribute('stroke-width', strokeWidth);
    path.setAttribute('fill', 'none');

    // Adds the path and time to the corresponding lists
    paths.push(path);
    times.push([event.timeStamp]);

    // Makes the path a part of the SVG, so the user can see the partially drawn stroke
    canvas.appendChild(path);
  }

  // Updates the current stroke with the newest part of the path
  function draw(event) {
    // Only draw if the user has the mouse button pressed
    if (!drawing) return;

    // Retrieves the current path
    const path = paths[paths.length - 1];

    // Retrieves the coordinates of the current path
    const d = path.getAttribute('d');
    
    // Adds the last part of the stroke and the last timeStamp to the corresponding lists
    path.setAttribute('d', `${d} L${event.offsetX},${event.offsetY}`);
    times[times.length - 1].push(event.timeStamp);
  }

  // Ends the current stroke
  function endDrawing() {
    if (!drawing) return;
    drawing = false;

    // Retrieve the current path
    const path = paths[paths.length - 1];

    // Extract the coordinates from the path
    const d = path.getAttribute('d').split(/[ML]/).filter(item => item !== '').map(point => point.trim().split(',').map(Number));

    // Remove the unsimplified path from the canvast
    paths.pop().remove();

    // Find the bending points of the simplified path
    findBendingPoints(d);  
  }

  // Get the drawn strokes
  window.getDrawnStrokes = function() {
    // Return the array of drawn strokes
    return paths; 
  };  
  
  // Simplify the path with the Ramer-Douglas-Peucker algorithm
  function simplifyPath(points, tolerance) {
    // If the stroke can't be simplified anymore, return
    if (points.length <= 2) {
      return points;
    }
  
    // Find the first and last point of the current stroke segment
    const [firstPoint, lastPoint] = [points[0], points[points.length - 1]];

    // Initialise values
    let maxDistance = 0;
    let index = 0;

    // For each point in the current stroke,
    for (let i = 1; i < points.length - 1; i++) {
      // find the largest perpendicular distance to find the largest outlier
      const distance = perpendicularDistance(points[i], firstPoint, lastPoint);

      if (distance > maxDistance) {
        maxDistance = distance;
        index = i;
      }
    }

    // If the largest outlier is larger than the tolerance,
    if (maxDistance > tolerance) {
      // reanalyse the left and the right parts of the stroke individually
      const leftPath = simplifyPath(points.slice(0, index + 1), tolerance);
      const rightPath = simplifyPath(points.slice(index), tolerance);

      // then merge them without duplicating the largest outlier
      return leftPath.slice(0, -1).concat(rightPath);
    } else {
      // else, return the simplified path
      return [firstPoint, lastPoint];
    }
  }
  
  // Calculate the distance between two points
  function calculateDistance(startPoint, endPoint) {
    const [x1, y1] = startPoint;
    const [x2, y2] = endPoint;

    const dx = x2 - x1;
    const dy = y2 - y1;

    // Euclidean distance formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    const distance = Math.abs(Math.sqrt(dx * dx + dy * dy));
    
    return distance;
  } 

  // Function to calculate perpendicular distance from a point to a line
  function perpendicularDistance(point, lineStart, lineEnd) {
    // Initialize the values
    const [px, py] = point;
    const [x1, y1] = lineStart;
    const [x2, y2] = lineEnd;

    // Find the distance between the start and end points
    const dx = x2 - x1;
    const dy = y2 - y1;

    // Find the perpendicular distance
    const distance = Math.abs(dy * px - dx * py + x2 * y1 - y2 * x1) / Math.sqrt(dx * dx + dy * dy);
    return distance;
  }

  // Find the bending points of the simplified stroke
  function findBendingPoints(path) {
    allFits = [];
    if (path.length === 0) return;
    
    // Compute the speed and curvature of the simplified path
    let speed = calculateSpeed(path);
    let curvature = calculateCurvature(path);

    // Find the maximal speed, and the average of the speed and curvature
    let maximalSpeed = speed.reduce((maximalSpeed, point) => Math.max(maximalSpeed, point.speed), 0);
    let averageSpeed = (speed.reduce((totalValue, point) => totalValue + point.speed, 0)/speed.length) * speedModifier;
    let averageCurvature = (curvature.reduce((totalValue, point) => totalValue + point.curvature, 0)/curvature.length) * curveModifier;
    
    // Filter the speed and curvature to match the thresholds
    let filteredSpeed = speed.filter(value => {
      return value.speed < averageSpeed;
    });
    let filteredCurvature = curvature.filter(value => {
      return value.curvature > averageCurvature;
    });

    let { intersection: intersection, speed: speedPoints, curvature: curvaturePoints } = findIntersection(filteredSpeed, filteredCurvature);
    if (intersection.length > 0) {
      intersection = intersection.concat([{ point: path[0], index: 0 }, { point: path[path.length - 1], index: path.length - 1 }]);
    } else {
      intersection = [{ point: path[0], index: 0 }, { point: path[path.length - 1], index: path.length - 1 }];
    }
    let minimalFit = findMinimalFit(intersection);
    
    minimalFit.sort((first, second) => first.index - second.index);

    let speedCertainty = normalizeCertainty(findSpeedCertainty(speedPoints, maximalSpeed));
    let curvatureCertainty = normalizeCertainty(findCurvatureCertainty(curvaturePoints,path));
    
    let bestFit = findBestFit(path, minimalFit, speedCertainty, curvatureCertainty).path;
    let bestFitArray = []

    for (let i = 0; i < bestFit.length; i++) {
      bestFitArray.push(bestFit[i].point);
    }

    bestFits.push(bestFitArray)

    displayBestFit(bestFit);
  }

  // Find the speed with which the stroke was drawn
  function calculateSpeed(path) {
    // Initialise variables
    const points = [];
    
    // For each part of the stroke,
    for (let i = 0; i < path.length - 1; i++) {
      // find the length and the drawing time to calculate the speed
      const distance = calculateDistance(path[i], path[i + 1])
      const time = (times[times.length - 1][i + 1] - times[times.length - 1][i]) / 1000; // Convert ms to s
      const speed = distance/time;
      points.push({ point: path[i], index: i, speed: speed});
    }
    
    return points;
  }

  // Find the curvature of the stroke
  function calculateCurvature(path) {
    // Initialize the variables
    const points = [];

    // For each neighborhood * 2 points in the path
    for (let i = neighborhood; i < path.length - neighborhood; i++) {
      // initialize the variables
      const [x1, y1] = path[i - neighborhood];
      const [x2, y2] = path[i + neighborhood];
      const [xi, yi] = path[i];

      // and calculate the curvature
      const curvature = Math.abs((x2 - x1) * (yi - y1) - (xi - x1) * (y2 - y1)) / Math.sqrt(Math.pow((x2 - x1), 2) + Math.pow((y2 - y1), 2));
      points.push({ point: path[i], index: i, curvature: curvature });
    }

    return points;
  }

  // Find the certainty for speed points
  function findSpeedCertainty(points, maximalSpeed) {
    // Find the speed certainty for each point
    points.forEach(value => {
      value.certainty = 1 - (value.speed/maximalSpeed);
    });
    
    return points;
  }

  // Find the certainty for curvature points
  function findCurvatureCertainty(points, path) {
    // Initialize the variables
    let distance;
    let curveLength;

    // For each point
    points.forEach(value => {
      // find the index in the path
      let index = path.findIndex(p => p === value.point);
      
      // If the neighborhood fits completely in the array
      if (index - neighborhood >= 0 && index + neighborhood < path.length) {
        // find the distance between the first and last point
        distance = calculateDistance(path[index - neighborhood], path[index + neighborhood]);
        
        // and the length of the curve in the neighborhood
        curveLength = 0;
        for (let i = index - neighborhood; i < index + neighborhood - 1; i++) {
             curveLength += calculateDistance(path[i], path[i + 1]);
        }

        // and calculate and store the certainty
        value.certainty = distance / curveLength;
      } else {
        value.certainty = 0;
      }
    });

    return points;
  }

  // Normalize the certainty values
  function normalizeCertainty(points) {
    // Find the minimal and maximal values for the certainty
    let minCertainty = points.reduce((minimal, point) =>  Math.min(minimal, point.certainty), 10);
    let maxCertainty = points.reduce((maximal, point) =>  Math.max(maximal, point.certainty), -10);

    // Normalize the values to a scale of [0, 1]
    points.forEach(value => {
      value.certainty = (value.certainty - minCertainty) / (maxCertainty - minCertainty)
    });

    // Sort points in decreasing order
    points.sort((first, second) => second.certainty - first.certainty);
    return points;
  }

  // Find the intersection between two arrays
  function findIntersection(speed, curvature) {
    // Initialize the values
    let intersection = []

    // For each point in the speed array
    speed.forEach(speedPoint => {
      // Try to find a match in the curvature array
      let found = curvature.find(curvaturePoint =>
        (speedPoint.point[0] == curvaturePoint.point[0] && speedPoint.point[1] == curvaturePoint.point[1])
      );
      
      if (found) {
        intersection.push({point: found.point, index: found.index});
      }
    });
    
    // Remove points from speed array if they are in the intersection
    speed = speed.filter(speedPoint => !intersection.some(intersectionPoint => 
      intersectionPoint.point[0] === speedPoint.point[0] &&
      intersectionPoint.point[1] === speedPoint.point[1]
    ));
    
    // Remove points from curvature array if they are in the intersection
    curvature = curvature.filter(curvaturePoint => !intersection.some(intersectionPoint => 
      intersectionPoint.point[0] === curvaturePoint.point[0] &&
      intersectionPoint.point[1] === curvaturePoint.point[1]
    ));
    
    return { intersection, speed, curvature };
  }

  function findMinimalFit(intersection) {
    let minimalFit = [];
    let closeIndexes = [];

    for (let i = 0; i < intersection.length - 1; i++) {
      if (calculateDistance(intersection[i].point, intersection[i + 1].point) < 30) {
        closeIndexes.push(i);
        closeIndexes.push(i + 1);
      } else if (!closeIndexes.includes(i)) {
        minimalFit.push(intersection[i]);
      }
    }
    
    // Handle the last point if it's not included in any close indexes
    if (!closeIndexes.includes(intersection.length - 1)) {
      minimalFit.push(intersection[intersection.length - 1]);
    }
    
    closeIndexes = closeIndexes.filter((first, second) => first === second);

    let index = 0;
    while (index < closeIndexes.length) {
      let start = index;
      
      while (index < closeIndexes.length - 1 && closeIndexes[index + 1] - closeIndexes[index] === 1) {
        index++;
      }

      let end = index;
      let middleIndex = Math.floor((closeIndexes[start] + closeIndexes[end]) / 2);
      minimalFit.push(intersection[middleIndex]);

      index++;
    }

    // Sort minimalFit to maintain order
    minimalFit.sort((first, second) => first.index - second.index);
    
    return minimalFit;
  }

  function findBestFit(path, minimalFit, speed, curvature) {
    let currentSpeedPath = minimalFit;
    for (let i = -1; i < speed.length; i++) {

      if (i >= 0) {
        currentSpeedPath = currentSpeedPath.concat(speed[i]);
      }

      let currentCurvaturePath = currentSpeedPath;
      for (let j = -1; j < curvature.length; j++) {
        if (!(i + j > 10)) {
          if (j >= 0) {
            currentCurvaturePath = currentCurvaturePath.concat(curvature[j]);
          }
          
          currentCurvaturePath.sort((first, second) => first.index - second.index);
          let fitError = findError(path, currentCurvaturePath);
          allFits.push({ path: currentCurvaturePath, error: fitError });
        }
      }
    }
    
    let newFits = allFits.filter(fit => fit.error < errorThreshold);
    if (newFits.length != 0) {
      allFits = newFits;
    }
    allFits.sort((first, second) => {
      if (first.path.length !== second.path.length) {
        return first.path.length - second.path.length;
      } else {
        return first.error - second.error;
      }});
    
    let finalFits = []
    while (allFits.length != 0) {
      let currentPath = allFits[0];
      finalFits.push(currentPath);
      allFits = allFits.filter(fit => fit.path.length > currentPath.path.length);
    }

    return finalFits[0];

    finalFits.sort((first, second) => first.error - second.error);
    for (let i = 0; i < finalFits.length - 1; i++) {
      if (finalFits[i + 1].error - finalFits[i].error > 5) {
        return finalFits[i]
      }
    }
    return finalFits[finalFits.length - 1]
  }

  function findError(path, currentFit) {
    // Initialize the values
    let sumSquaredDistances = 0;

    // For each part of the path
    for (let i = 0; i < path.length; i++) {
      let distance = 0;
      // Square the perpendicular distance to the point
      for (let j = 0; j < currentFit.length - 1; j++) {
        if (currentFit[j].index <= i && i <= currentFit[j + 1].index) {
          distance = perpendicularDistance(path[i], currentFit[j].point, currentFit[j + 1].point);
        }
      }
      sumSquaredDistances += distance * distance;
    }

    // Calculate the error of the point
    let error = sumSquaredDistances / path.length;
    return error;
  }

  // Display the best fit
  function displayBestFit(bestFit) {
    // Create a new SVG element (a path)
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    const d = bestFit.map((point, index) => {
      const command = index === 0 ? 'M' : 'L'; // Use 'M' for the first point, 'L' for subsequent points
      return `${command}${point.point.join(',')}`;
    }).join(' ');
    path.setAttribute('d', d);
    path.setAttribute('stroke', 'black'); // Use a different color for simplified paths
    path.setAttribute('stroke-width', strokeWidth);
    path.setAttribute('fill', 'none');
    
    // Add the path to the array
    bestFitsSVG.push(path); 

    // Show the path on the canvas
    canvas.appendChild(path);
    return path;
  } 
