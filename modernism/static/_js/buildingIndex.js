let filterList = [];
let selectedFilter = {};
let filterDescriptionContainer = document.querySelector("#filter-description");
const checkboxes = document.querySelectorAll('input[type=checkbox]');
const featureSelectFilter = document.querySelectorAll('.feature-select');
const dropdownFilter = document.querySelectorAll('.dropdown-custom');
const dropdownTriggers = document.querySelectorAll('.dropdown-trigger');
const dropdownMenus = document.querySelectorAll('.menu');
const resetFilterButton = document.querySelector('#reset-filter-btn');
const applyFilterButton = document.querySelector('#apply-filter-btn');

const getOptionKeyByEventTargetValue = (object, value) => {
    return Object.keys(object).find(key => object[key].value === value);
}

const renderFilterSelection = (selectedFilter) => {
    let filterList = Object.values(selectedFilter);
    let filterString = "";
    filterList.forEach(filter => {
        filterString += filter;
    })
    filterDescriptionContainer.innerHTML = filterString;
}

// ToDo: Set active color for feature dropdown
const toggleMenuButtonColor = (trigger) => {
    if (trigger.parentElement.querySelector(".menu").querySelectorAll('input[type=checkbox]:checked').length > 0) {
        let menuButton = trigger.parentElement.querySelector(".button");
        menuButton.classList.add("has-filter-set");
    } else {
        let menuButton = trigger.parentElement.querySelector(".button");
        menuButton.classList.remove("has-filter-set");
    }
}

const activateFilterButtons = () => {
    dropdownTriggers.forEach(trigger => {
        toggleMenuButtonColor(trigger);
    })
}

const addChangeEventListenerToFilterForm = () => {
    featureSelectFilter.forEach(selectField => {
        selectField.addEventListener('change', (event) => {
            event.preventDefault();
            if (event.target.value == "") {
                delete selectedFilter[event.target.id];
            } else {
                let optionKey = getOptionKeyByEventTargetValue(selectField.children, event.target.value)
                let filterValue = selectField.children[optionKey].innerText.trim()
                let hashTagString = "#" + filterValue + " ";
                if (selectField.name === "protected_monument") {
                    hashTagString = "#" + "Protected:" + filterValue + " ";
                }
                if (selectField.name === "storey") {
                    hashTagString = "#" + "Storey:" + filterValue + " ";
                }
                selectedFilter[event.target.id] = hashTagString;
            }
            renderFilterSelection(selectedFilter);
        });
    })

    checkboxes.forEach(box => {
        let filterValue = box.parentElement.innerText.trim();
        box.addEventListener('change', (event) => {
            event.preventDefault();
            if (box.checked) {
                let hashTagString = "#" + filterValue + " ";
                selectedFilter[event.target.id] = hashTagString;
            } else {
                delete selectedFilter[event.target.id];
            }
            renderFilterSelection(selectedFilter);
        });
    })
};

const collectAllSelectedFilter = () => {
    checkboxes.forEach(box => {
        let filterValue = box.parentElement.innerText.trim();
        if (box.checked) {
            let hashTagString = "#" + filterValue + " ";
            selectedFilter[box.id] = hashTagString;
        }
        renderFilterSelection(selectedFilter);
    });
    featureSelectFilter.forEach(selectField => {
        for (option of selectField) {
            if (option.selected && option.value) {
                let optionKey = getOptionKeyByEventTargetValue(selectField.children, option.value)
                let filterValue = selectField.children[optionKey].innerText.trim()
                let hashTagString = "#" + filterValue + " ";
                if (selectField.name === "protected_monument") {
                    hashTagString = "#" + "Protected:" + filterValue + " ";
                }
                if (selectField.name === "storey") {
                    hashTagString = "#" + "Storey:" + filterValue + " ";
                }
                selectedFilter[selectField.id] = hashTagString;
            }
        }
        renderFilterSelection(selectedFilter);
    });
}

const addEventListenerToDropdownFilter = () => {
    dropdownFilter.forEach(dropdown => {
        let trigger = dropdown.querySelector(".dropdown-trigger");
        let menu = dropdown.querySelector(".menu");

        trigger.addEventListener('click', (event) => {
            event.preventDefault();
            dropdownMenus.forEach(dropMenu => {
                dropMenu.classList.add("is-hidden");
            })
            if (Array.from(trigger.classList).includes("is-active")) {
                dropdownTriggers.forEach(trigger => {
                    trigger.classList.remove("is-active");
                    toggleMenuButtonColor(trigger);
                })
            } else {
                dropdownTriggers.forEach(trigger => {
                    trigger.classList.remove("is-active");
                    toggleMenuButtonColor(trigger);
                })
                trigger.classList.add("is-active");
                menu.classList.remove("is-hidden");
            }
        });
    })
}

const resetFilters = () => {
    checkboxes.forEach(box => {
        box.checked = false;
    });
    featureSelectFilter.forEach(selectField => {
        let allOptions = selectField.options;
        for (var i = 0; i < allOptions.length; i++) {
            allOptions[i].selected = false;
        }
    });
}

const addEventListenerToResetFilterButton = () => {
    resetFilterButton.addEventListener('click', (event) => {
        event.preventDefault();
        resetFilters();
        applyFilterButton.click();
    })
}

addChangeEventListenerToFilterForm();
collectAllSelectedFilter();
addEventListenerToDropdownFilter();
addEventListenerToResetFilterButton();
activateFilterButtons();