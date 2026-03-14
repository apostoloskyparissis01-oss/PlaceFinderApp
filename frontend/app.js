document.getElementById('search-form').addEventListener('submit',function(e){
    e.preventDefault();

    const userlocation = document.getElementById('location').value;
    const radius = document.getElementById('radius').value;
    const cuisine = document.getElementById('cuisine').value;
    const budget = document.getElementById('budget').value;

    const url = `http://127.0.0.1:8080/places?location=${userlocation}&radius=${radius}&cuisine=${cuisine}&budget=${budget}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const results = data.results;
            const resultDiv = document.getElementById('results');
            resultDiv.innerHTML='';

            results.forEach((place,index) => {
                const card = document.createElement('div');
                card.className = 'card';
                card.style.animationDelay = `${index * 0.1}s`;
                card.innerHTML = `
                <h3>${place.name}</h3>
                <p>⭐ ${place.rating}</p>
                <p>📍 ${place.vicinity}</p>
                `;
                resultDiv.appendChild(card);   
                
            });
        
    });


});


