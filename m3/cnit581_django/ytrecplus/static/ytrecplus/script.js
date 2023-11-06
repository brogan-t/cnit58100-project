document.addEventListener('DOMContentLoaded', function () {
    const dropdownButtons = document.querySelectorAll('.dropdown-button');
    
    dropdownButtons.forEach(button => {
        button.addEventListener('click', function () {
            const dropdownMenu = this.nextElementSibling; // Get the dropdown menu next to the button
            dropdownMenu.classList.toggle('dropdown-menu-show'); // Toggle the 'dropdown-menu-show' class to open/close the dropdown
        });
    });

    // Close the dropdown when clicking outside of it
    window.addEventListener('click', function (event) {
        if (!event.target.matches('.dropdown-button')) {
            const dropdowns = document.querySelectorAll('.dropdown-menu');
            dropdowns.forEach(dropdown => {
                if (dropdown.classList.contains('dropdown-menu-show')) {
                    dropdown.classList.remove('dropdown-menu-show');
                }
            });
        }
    });
	
	/* Add event handlers for the popup menu */
	const openPopupButton = document.getElementById('openPopup');
    const closePopupButton = document.getElementById('closePopup');
    const popupContainer = document.getElementById('popupContainer');

    openPopupButton.addEventListener('click', function () {
        popupContainer.style.display = 'flex';
    });

    closePopupButton.addEventListener('click', function () {
        popupContainer.style.display = 'none';
    });
});