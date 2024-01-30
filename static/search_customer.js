const resultBox = document.querySelector('.result-box');
const inputBox = document.getElementById('input-box');
resultBox.innerHTML = '';

let selectedIdx = -1;

function selectInput(list) {
    inputBox.value = list.innerHTML;
    resultBox.innerHTML = '';
}

fetch('http://127.0.0.1:5000/api/customers')
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


document.getElementById('search_customer').addEventListener('click', function(){
    var inputValue = encodeURIComponent(document.getElementById('input-box').value);

    var url = "http://127.0.0.1:5000/edit_cust/" + inputValue;

    window.location.href = url;

})