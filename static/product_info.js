const input = document.getElementById('input');
const autocompleteList = document.getElementById('autocomplete-list');
autocompleteList.innerHTML = '';

fetch('http://127.0.0.1:5000//api/data')
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




const resultBox = document.querySelector('.result-box');
const inputBox = document.getElementById('input-box');
function selectInput(list) {
    inputBox.value = list.innerHTML;
    resultBox.innerHTML = '';
}
resultBox.innerHTML = '';


fetch('http://127.0.0.1:5000//api/data')
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


document.getElementById('deleteLink').addEventListener('click', function() {
    var inputValue = encodeURIComponent(document.getElementById('input').value);

    var url = "http://127.0.0.1:5000/product_info_2/" + inputValue;

    window.location.href = url;
});


// Get references to the input field and the link
const inputField = document.getElementById('input');
const deleteLink = document.getElementById('deleteLink');

// Add an event listener to the input field
inputField.addEventListener('input', function() {
// Check if the input value is not empty
if (inputField.value.trim() !== '') {
    // If not empty, show the link
    deleteLink.style.display = 'block';
} else {
    // If empty, hide the link
    deleteLink.style.display = 'none';
}
});