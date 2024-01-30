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