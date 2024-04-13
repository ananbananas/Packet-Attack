// vim: ts=2 sts=2 sw=2 et
const box = document.getElementById('box');
let inter;
let accel_X = 3;
let accel_Y = 3;
let vel_X = 1;
let vel_Y = 1;

function refresh() {
  const posX = parseInt(box.style.left) || 0;
  const posY = parseInt(box.style.top) || 0;
  if (posX + box.clientWidth >= window.innerWidth) {
    vel_X = -Math.floor(Math.random() * accel_X);
  } else if (posX <= 0) {
    vel_X = Math.floor(Math.random() * accel_X);
  }
  if (posY + box.clientHeight >= window.innerHeight) {
    vel_Y = -Math.floor(Math.random() * accel_Y);
  } else if (posY <= 0) {
    vel_Y = Math.floor(Math.random() * accel_Y);
  }
  box.style.left = `${posX + vel_X}px`;
  box.style.top = `${posY + vel_Y}px`;
}

async function attack() {
  const resp = await fetch('/attack');
  if (!resp.ok) {
    return;
  }
  clearInterval(inter);
  const imgBytes = await resp.arrayBuffer();
  const img = new Blob([imgBytes], {type: resp.headers.get('Content-Type')});
  const imgEl = document.createElement('img');
  imgEl.src = URL.createObjectURL(img);
  imgEl.width = 200;
  imgEl.height = 200;
  box.textContent = resp.status === 201 ? 'data is secured' : '';
  box.appendChild(imgEl);
}

async function upload() {
  document.getElementById('box').style.left = '0';
  const file = document.getElementById('file').files[0];
  const formData = new FormData();
  formData.append('file', file);
  console.log('value', document.getElementById('protocol').value);
  const resp = await fetch(`/upload?proto=${document.getElementById('protocol').value}`, {
    method: 'POST',
    body: formData,
  });
  if (!resp.ok) {
    console.error('upload failed');
  }
  box.textContent = 'data packet';
  inter = setInterval(() => {
    setTimeout(() => {}, 1000);
    refresh();
  });
}

window.upload = upload
window.attack = attack
