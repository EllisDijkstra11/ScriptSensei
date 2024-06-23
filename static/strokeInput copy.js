document.addEventListener('DOMContentLoaded', function () {
  // Get the IDs of interactive elements
  const canvas = document.getElementById('canvas');
  const clearButton = document.getElementById('clear');

  // Initialize values
  let drawing = false;
  let paths = [];
  let simplifiedPaths = [];
  let times = [];

  // Set values for the physical appearance of the strokes
  const tolerance = 2;
  const strokeWidth = 2;

  // Add eventListeners to recognize the strokes
  canvas.addEventListener('mousedown', startDrawing);
  canvas.addEventListener('mousemove', draw);
  canvas.addEventListener('mouseup', endDrawing);
  canvas.addEventListener('mouseleave', endDrawing);

  // Add an eventListener to clear the canvas
  clearButton.addEventListener('click', clearCanvas);

  // Create a new path to store the stroke
  function startDrawing(event) {
    drawing = true;

    // Create a new SVG element (a path)
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', `M${event.offsetX},${event.offsetY}`);
    path.setAttribute('stroke', 'black');
    path.setAttribute('stroke-width', strokeWidth);
    path.setAttribute('fill', 'none');

    console.log(path)
    console.log(paths)
    // Adds the path and time to the corresponding lists
    paths.push(path);
    console.log(paths)
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
    drawing = false;

    console.log(paths)
    // Retrieve the current path
    const path = paths[paths.length - 1];
    console.log(path)

    // Extract the coordinates from the path
    const d = path.getAttribute('d').split(/[ML]/).filter(item => item !== '').map(point => point.trim().split(',').map(Number));
    console.log(d)

    // Simplify the path
    const simplifiedPath = simplifyPath(d, tolerance);
    console.log(simplifiedPath)

    // Remove the unsimplified path from the canvast
    paths.pop().remove();

    // Display the simplified path
    displaySimplifiedPath(simplifiedPath);

    // Compute the speed and curvature of the simplified path
    computeSpeedAndCurvature(simplifiedPath)
  }

  // Remove all paths from the canvas and lists
  function clearCanvas() {
    // Remove all paths from the canvas
    paths.forEach(path => path.remove());
    simplifiedPaths.forEach(path => path.remove());

    // Empty all lists
    paths = [];
    simplifiedPaths = [];
    times = [];
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

  // Display the simplified path
  function displaySimplifiedPath(simplifiedPath) {
    // Create a new SVG element (a path)
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    console.log(simplifiedPath)
    const d = simplifiedPath.map((point, index) => (index === 0 ? 'M' : 'L') + point.join(',')).join(' ');    path.setAttribute('d', d);
    path.setAttribute('stroke', 'black'); // Use a different color for simplified paths
    path.setAttribute('stroke-width', strokeWidth);
    path.setAttribute('fill', 'none');
    
    // Add the simplified path to the array
    simplifiedPaths.push(path); 

    // Show the path on the canvas
    canvas.appendChild(path);
    return path;
  }  

  // Function to calculate perpendicular distance from a point to a line
  function perpendicularDistance(point, lineStart, lineEnd) {
    // Initialize the values
    const [x1, y1] = lineStart;
    const [x2, y2] = lineEnd;
    const [px, py] = point;

    // Find the distance between the start and end points
    const dx = x2 - x1;
    const dy = y2 - y1;

    // Find the perpendicular distance
    const distance = Math.abs(dy * px - dx * py + x2 * y1 - y2 * x1) / Math.sqrt(dx * dx + dy * dy);
    return distance;
  }

  function computeSpeedAndCurvature(path) {
    const speed = [];
    const curvature = [];
    const k = 3; // Neighborhood size

    for (let i = 1; i < path.length; i++) {
      const [x1, y1] = path[i - 1];
      const [x2, y2] = path[i];
      const distance = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
      const time = (times[times.length - 1][i] - times[times.length - 1][i - 1]) / 1000; // Convert ms to s
      speed.push(distance / time);
    }

    for (let i = k; i < path.length - k; i++) {
      const [x1, y1] = path[i - k];
      const [x2, y2] = path[i + k];
      const [xi, yi] = path[i];

      const curvatureValue = Math.abs((x2 - x1) * (yi - y1) - (xi - x1) * (y2 - y1)) / Math.sqrt(Math.pow((x2 - x1), 2) + Math.pow((y2 - y1), 2));
      curvature.push(curvatureValue);
    }

    console.log('Speed:', speed);
    console.log('Curvature:', curvature);
  }
});