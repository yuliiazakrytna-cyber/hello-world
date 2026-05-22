let count = 0;
const btn = document.getElementById('btn');
const counter = document.getElementById('counter');

btn.addEventListener('click', () => {
  count++;
  counter.textContent = count === 1 ? 'Clicked 1 time' : `Clicked ${count} times`;
});
