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



window.onload = function() {
    var specificPointElement = document.getElementById('specificPoint');

    // Check if the element exists
    if (specificPointElement) {
        specificPointElement.scrollIntoView();
    }
};

const form2 = document.getElementById('myForm2');
const provider_input = document.getElementById('input-box');
const amount_input = document.getElementById('amount');
const submitButton2 = document.getElementById('file_exb2');


form2.addEventListener('input', checkFormCompleteness);

function checkFormCompleteness() {
    const providerValue = provider_input.value.trim();
    const amountValue = amount_input.value.trim();


    const allFormsComplete = providerValue !== '' && amountValue !== '';

    // Show or hide the submit button based on the completeness of the form
    submitButton2.disabled = !allFormsComplete;
    submitButton2.style.display = allFormsComplete ? 'block' : 'none';
}