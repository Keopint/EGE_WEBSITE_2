document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.container');

  container.addEventListener('click', (event) => {
      if (event.target.classList.contains('remove')) {
          const unit = event.target.closest('.unit');
          if (document.querySelectorAll('.unit').length > 1) {
              unit.remove();
          }
      } else if (event.target.classList.contains('add')) {
          const unit = event.target.closest('.unit');
          const newUnit = createUnit();
          unit.insertAdjacentElement('afterend', newUnit);
      }
  });

  function createUnit() {
      const div = document.createElement('div');
      div.className = 'unit';
      div.innerHTML = `
          <input type="text" class="name" placeholder="Name">
          <input type="text" class="link" placeholder="Link">
          <button class="remove">Rm</button>
          <button class="add">Add</button>
      `;
      makeDraggable(div);
      return div;
  }

  function makeDraggable(unit) {
      unit.draggable = true;

      unit.addEventListener('dragstart', () => {
          unit.classList.add('dragging');
      });

      unit.addEventListener('dragend', () => {
          unit.classList.remove('dragging');
      });

      container.addEventListener('dragover', (event) => {
          event.preventDefault();
          const draggingUnit = document.querySelector('.dragging');
          const belowUnit = getDragAfterElement(container, event.clientY);

          if (belowUnit == null) {
              container.appendChild(draggingUnit);
          } else {
              container.insertBefore(draggingUnit, belowUnit);
          }
      });
  }

  function getDragAfterElement(container, y) {
      const draggableUnits = [...container.querySelectorAll('.unit:not(.dragging)')];

      return draggableUnits.reduce((closest, child) => {
          const box = child.getBoundingClientRect();
          const offset = y - box.top - box.height / 2;
          if (offset < 0 && offset > closest.offset) {
              return { offset: offset, element: child };
          } else {
              return closest;
          }
      }, { offset: Number.NEGATIVE_INFINITY }).element;
  }

  // Make existing units draggable
  document.querySelectorAll('.unit').forEach(makeDraggable);
});

function getUnitData() {
  const units = document.querySelectorAll('.unit');
  const dataArray = [];

  units.forEach((unit) => {
      const name = unit.querySelector('.name').value;
      const link = unit.querySelector('.link').value;
      dataArray.push({ name, link });
  });

  return dataArray;
}

async function update_cource() {
  try {
      const currentUrl = window.location.origin + "/api/update_course/" + course_id;
      data = {"data": getUnitData()};

      const response = await fetch(currentUrl, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      });
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
  } catch (error) {
      console.error('Error sending POST request:', error);
  }
}