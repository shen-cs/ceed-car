const RADIUS = 30;
const LEN_SCALE = 35;
const ARROW_ANGLE = 20 / 180 * Math.PI;
const ARROW_LEN = 0.5 * LEN_SCALE;
const X_START = 500;
const Y_START = 600;

const drawNode = (ctx, id, loc) => {
  const { x, y } = loc;
  ctx.beginPath();
  ctx.arc(x, y, RADIUS, 0, 2* Math.PI);
  ctx.stroke();
  ctx.font = '20px century';
  ctx.textAlign = 'center';
  ctx.fillStyle = '#000';
  ctx.textBaseline="middle";
  ctx.fillText(id, x, y);
  ctx.closePath();
}

const drawLine = (ctx, start_loc, end_loc, text) => {
  ctx.beginPath();
  ctx.moveTo(start_loc.x, start_loc.y);
  ctx.lineTo(end_loc.x, end_loc.y);
  ctx.stroke();
  ctx.font = '25px century';
  ctx.textAlign = 'center';
  ctx.fillStyle = '#2196F3';
  ctx.textBaseline="middle";
  ctx.fillText(text, (start_loc.x + end_loc.x) / 2, (start_loc.y + end_loc.y) / 2)
  ctx.closePath();
}

const drawArrowLine = (ctx, start_loc, end_loc, text) => {
  drawLine(ctx, start_loc, end_loc, text);
  const gamma = Math.atan2(end_loc.y - start_loc.y, end_loc.x - start_loc.x);
  const angle = 2 * Math.PI / 2 - gamma - ARROW_ANGLE;
  const arrow_loc_1 = {x: end_loc.x + ARROW_LEN * Math.cos(angle), y: end_loc.y - ARROW_LEN * Math.sin(angle)};
  const arrow_loc_2 = {x: end_loc.x + ARROW_LEN * Math.cos(angle+2*ARROW_ANGLE), y: end_loc.y - ARROW_LEN * Math.sin(angle+2*ARROW_ANGLE)};
  drawLine(ctx, end_loc, arrow_loc_1, "");
  drawLine(ctx, end_loc, arrow_loc_2, "");
}

// info == [len, angle]
const convertPos = (x, y, info) => {
  return [x + info[0] * Math.sin(info[1]), y - info[0] * Math.cos(info[1])];
}

const drawMap = (ctx, map) => {
  console.clear();
  map = JSON.parse(map);
  const nodeKeys = Object.keys(map);
  let queue = [nodeKeys[0]];
  let x = X_START, y = Y_START;
  let graph = {};
  while(queue && queue.length) {
    const nodeId = queue.shift();
    // console.log(queue.length);
    if(graph.hasOwnProperty(nodeId)) {
      x = graph[nodeId].x;
      y = graph[nodeId].y;
    }
    else {
      console.assert(x === X_START && y === Y_START, 'pos does not match!!' );
      console.log('Adding', nodeId);
      graph[nodeId] = {x, y};
    }
    for(let neighborId in map[nodeId]) {
      const info = map[nodeId][neighborId];
      const len = info[0] * LEN_SCALE;
      const angle = info[1] / 180 * Math.PI;
      const newPos = convertPos(x, y, [len, angle]);
      const newX = newPos[0];
      const newY = newPos[1];
      const startPos = convertPos(x, y, [RADIUS, angle]);
      drawLine(ctx, {x: startPos[0], y: startPos[1]}, {x: newX, y: newY}, info[0]);
      
      if(!graph.hasOwnProperty(neighborId)) {
        queue.push(neighborId);
        const nodePos = convertPos(newX, newY, [RADIUS, angle]);
        console.log('Adding', neighborId);
        graph[neighborId] = {x: nodePos[0], y: nodePos[1]};
      }
    }
  }
  for(let nodeId in graph) {
    drawNode(ctx, nodeId, graph[nodeId])
  }
};

const drawPath = (ctx, path) => {
  path = JSON.parse(path);
  const startId = path["header"]["start"];
  let x = 50, y = 100;
  let toDraw = startId;
  while(true) {
    console.log(toDraw);
    drawNode(ctx, toDraw, {x, y});
    toDraw = path[toDraw]["next"];
    if(!toDraw) {
      break;
    }
    drawArrowLine(ctx, {x: x + 10 + RADIUS , y}, {x: x + 50 + RADIUS, y}, "");
    x += (2 * RADIUS + 60);
    if(x > 600) {
      x = 50;
      y += 100;
    }
  }
};

export { drawMap, drawPath };
