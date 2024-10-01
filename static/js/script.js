document.addEventListener('DOMContentLoaded', function () {
    // Модальные окна
    const contactModal = document.getElementById('contact-modal');
    const accessibilityModal = document.getElementById('accessibility-modal');
    const userModal = document.getElementById('user-modal');
    const modals = [contactModal, accessibilityModal, userModal];

    // Кнопки для открытия модальных окон
    const contactsLink = document.getElementById('contacts-link');
    const accessibilityBtn = document.getElementById('accessibility-settings-btn');
    const userSettingsBtn = document.getElementById('user-settings-btn');

    // Открытие модальных окон
    contactsLink.addEventListener('click', function () {
        contactModal.style.display = 'block';
    });

    accessibilityBtn.addEventListener('click', function () {
        accessibilityModal.style.display = 'block';
    });

    userSettingsBtn.addEventListener('click', function () {
        userModal.style.display = 'block';
    });

    // Закрытие модальных окон
    modals.forEach(modal => {
        const closeBtn = modal.querySelector('.close');
        closeBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    });

    // Закрытие модальных окон при клике вне их области
    window.addEventListener('click', function (event) {
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
});

/*я непон нужно ли на данном этапе верхняя часть, это и чуть ниже нужно для плавного раскрывания настроек */
document.addEventListener('DOMContentLoaded', function() {
    const dropdownBtn = document.querySelector('.dropbtn');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdownBtn.addEventListener('click', function(e) {
        e.preventDefault();
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });

    // Закрыть меню при клике вне области
    window.addEventListener('click', function(e) {
        if (!e.target.matches('.dropbtn')) {
            dropdownContent.style.display = 'none';
        }
    });
});
