const resultBox = document.querySelector('.result-box');
const inputBox = document.getElementById('input-box');
function selectInput(list) {
    inputBox.value = list.innerHTML;
    resultBox.innerHTML = '';
}
resultBox.innerHTML = '';


fetch('http://127.0.0.1:5000//api/fz')
.then(response => response.json())
.then(availableKeywords => {
    availableKeywords = availableKeywords['resp'];
    inputBox.addEventListener('input', function () {
        var inputValueLength = inputBox.value.length;

        if (inputValueLength === 0) {
            resultBox.innerHTML = '';
        } else {
            let result = availableKeywords.filter((keyword) => {
                return keyword.toLowerCase().includes(inputBox.value.toLowerCase());
            });

            display(result);
        }
    });

    inputBox.addEventListener('keydown', function (event) {
        const resultItems = resultBox.querySelectorAll('li');

        if (event.key === 'ArrowDown' && selectedIdx < resultItems.length - 1) {
            selectedIdx++;
        } else if (event.key === 'ArrowUp' && selectedIdx > 0) {
            selectedIdx--;
        } else if (event.key === 'Enter' && selectedIdx !== -1) {
            selectInput(resultItems[selectedIdx]);
        }

        if (resultItems.length > 0) {
            resultItems.forEach((item, index) => {
                if (index === selectedIdx) {
                    item.classList.add('selected');
                    inputBox.value = item.innerHTML; // Update inputBox with the selected suggestion
                } else {
                    item.classList.remove('selected');
                }
            });
        }
    });

    function display(result) {
        const content = result.map((list) => {
            return "<li onclick=selectInput(this)>" + list + '</li>';
        });

        resultBox.innerHTML = '<ul>' + content.join('') + '</ul>';
        selectedIdx = -1; // Reset selected index when displaying new results
    }
})
.catch(error => {
    console.error('Error fetching data:', error);
});






const input = document.getElementById('input');
const autocompleteList = document.getElementById('autocomplete-list');
autocompleteList.innerHTML = '';

fetch('http://127.0.0.1:5000//api/fz')
    .then(response => response.json())
    .then(options => {
        options = options['resp'];

        input.addEventListener('input', function () {
            const searchTerm = input.value.toLowerCase();

            if (searchTerm === '') {
                autocompleteList.innerHTML = ''; // Clear the autocomplete list
                return;
            }

            const filteredOptions = options.filter(option =>
                option.toLowerCase().includes(searchTerm)
            );

            displayAutocomplete(filteredOptions);
        });

        function displayAutocomplete(filteredOptions) {
            autocompleteList.innerHTML = '';

            filteredOptions.forEach(option => {
                const li = document.createElement('li');
                li.textContent = option;
                li.addEventListener('click', function () {
                    input.value = option;
                    autocompleteList.innerHTML = '';
                });
                autocompleteList.appendChild(li);
            });
        }
    });




    
const form = document.getElementById('myForm');
const dateInput = document.getElementById('dateInput');
const invoiceInput = document.getElementById('invoiceInput');
const delegateInput = document.getElementById('delegateInput');
const providerInput = document.getElementById('input');
const submitButton = document.getElementById('file_exb');

form.addEventListener('input', checkFormCompleteness);

function checkFormCompleteness() {
    const dateValue = dateInput.value.trim();
    const invoiceValue = invoiceInput.value.trim();
    const delegateValue = delegateInput.value.trim();
    const providerValue = providerInput.value.trim();

    const allFormsComplete = dateValue !== '' && invoiceValue !== '' && delegateValue !== '' && providerValue !== '';

    // Show or hide the submit button based on the completeness of the form
    submitButton.style.display = allFormsComplete ? 'block' : 'none';
}

const form2 = document.getElementById('myForm2');
const dateInput2 = document.getElementById('dateInput2');
const invoiceInput2 = document.getElementById('invoiceInput2');
const delegateInput2 = document.getElementById('delegateInput2');
const providerInput2 = document.getElementById('input-box');
const submitButton2 = document.getElementById('file_exb2');

form2.addEventListener('input', checkFormCompleteness2);

function checkFormCompleteness2() {
    const dateValue = dateInput2.value.trim();
    const invoiceValue = invoiceInput2.value.trim();
    const delegateValue = delegateInput2.value.trim();
    const providerValue = providerInput2.value.trim();

    const allFormsComplete = dateValue !== '' && invoiceValue !== '' && delegateValue !== '' && providerValue !== '';

    // Show or hide the submit button based on the completeness of the form
    submitButton2.disabled = !allFormsComplete;
    submitButton2.style.display = allFormsComplete ? 'block' : 'none';
}



document.getElementById('month_input').addEventListener('input', function() {
    var inputValue = this.value;
    var button = document.getElementById('f_b');
    
    if (inputValue) {
        button.disabled = false;
    } else {
        button.disabled = true;
    }
});

document.getElementById('dowload_date').addEventListener('input', function() {
    var inputValue = this.value;
    var button = document.getElementById('down_button');
    
    if (inputValue) {
        button.disabled = false;
    } else {
        button.disabled = true;
    }
});