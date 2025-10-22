// File: /geoprocessamento-2/geoprocessamento-2/scripts/svg-interactions.js

document.addEventListener('DOMContentLoaded', function() {
    // Function to handle mouseover events on SVG elements
    function handleMouseOver(event) {
        const target = event.target;
        if (target.tagName === 'path' || target.tagName === 'circle' || target.tagName === 'rect') {
            target.style.fill = '#FFCC00'; // Change color on hover
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.innerText = target.getAttribute('data-info'); // Assuming data-info attribute contains info
            document.body.appendChild(tooltip);
            tooltip.style.left = `${event.pageX}px`;
            tooltip.style.top = `${event.pageY}px`;
        }
    }

    // Function to handle mouseout events on SVG elements
    function handleMouseOut(event) {
        const target = event.target;
        if (target.tagName === 'path' || target.tagName === 'circle' || target.tagName === 'rect') {
            target.style.fill = ''; // Reset color
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        }
    }

    // Function to handle click events on SVG elements
    function handleClick(event) {
        const target = event.target;
        if (target.tagName === 'path' || target.tagName === 'circle' || target.tagName === 'rect') {
            alert(`You clicked on: ${target.getAttribute('data-name')}`); // Assuming data-name attribute contains name
        }
    }

    // Attach event listeners to all SVG elements
    const svgElements = document.querySelectorAll('svg path, svg circle, svg rect');
    svgElements.forEach(element => {
        element.addEventListener('mouseover', handleMouseOver);
        element.addEventListener('mouseout', handleMouseOut);
        element.addEventListener('click', handleClick);
    });
});