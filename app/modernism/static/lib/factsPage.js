const addClickEventListenerToFactCards = () => {
    const factCards = document.querySelectorAll('.fact-card');
    const html = document.getElementsByTagName('html')[0];
    factCards.forEach(card => {
        card.addEventListener('click', event => {
            event.preventDefault();
            card.nextElementSibling.classList.toggle('is-active');
            html.classList.toggle('is-clipped');
        });
    });
};

const addClickEventListenerToModalCards = () => {
    const closeButtons = document.querySelectorAll('.close-button');
    const html = document.getElementsByTagName('html')[0];
    console.log(html);
    closeButtons.forEach(button => {
        button.addEventListener('click', event => {
            event.preventDefault();
            button.parentElement.parentElement.parentElement.classList.remove('is-active');
            html.classList.remove('is-clipped');
        });
    });
};

addClickEventListenerToFactCards();
addClickEventListenerToModalCards();