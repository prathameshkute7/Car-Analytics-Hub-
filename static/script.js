let allCarsData = {};
let myChart = null;

// On page load, the old load function runs along with the new features
window.onload = function() {
    // 1. Load single car data (your original functionality)
    loadCarData();

    // 2. Fetch all data at once for advanced features (chart, filter, comparison)
    fetch('/get_all_data')
    .then(res => res.json())
    .then(data => {
        allCarsData = data;
        populateDropdowns(Object.keys(data));
        loadComparison();
        buildChart();
    })
    .catch(err => console.error("Error loading advanced data:", err));
};

// Your original function (for loading single car data)
function loadCarData() {
    const selectedCar = document.getElementById('carSelect').value;

    fetch('/get_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ car_name: selectedCar })
    })
    .then(response => response.json())
    .then(res => {
        if(res.status === 'success') {
            const data = res.data;
            
            // Left Panel content
            document.getElementById('carTitle').innerText = selectedCar;
            document.getElementById('tableBrand').innerText = data.brand;
            document.getElementById('tableType').innerText = data.type;
            document.getElementById('tablePrice').innerText = data.price;
            document.getElementById('carDesc').innerText = data.desc; // Load description

            // Performance Bar updates
            document.getElementById('hpValue').innerText = data.hp + " HP";
            document.getElementById('hpBar').style.width = (data.hp / 250 * 100) + '%';

            document.getElementById('speedValue').innerText = data.top_speed + " km/h";
            document.getElementById('speedBar').style.width = (data.top_speed / 250 * 100) + '%';

            // New Detailed Specs content
            document.getElementById('infoEngine').innerText = data.engine;
            document.getElementById('infoFuel').innerText = data.fuel;
            document.getElementById('infoMileage').innerText = data.mileage_str || data.mileage; // Display string mileage
            document.getElementById('infoSeats').innerText = data.seats;
            document.getElementById('infoSafety').innerText = data.safety;
        }
    })
    .catch(err => console.error("Error fetching data:", err));
}

// --- New feature code starts here ---

// Dynamically populate both comparison dropdowns
function populateDropdowns(carNames) {
    const s1 = document.getElementById('carSelect1');
    const s2 = document.getElementById('carSelect2');
    
    if(!s1 || !s2) return; // No error if these elements don't exist in HTML yet

    s1.innerHTML = '';
    s2.innerHTML = '';

    carNames.forEach((name) => {
        s1.options[s1.options.length] = new Option(name, name);
        s2.options[s2.options.length] = new Option(name, name);
    });

    if(carNames.length > 1) s2.selectedIndex = 1; // Second car selected by default
}

// Logic to apply budget and type filters
function applyFilters() {
    const selectedType = document.getElementById('typeFilter').value;
    const maxBudget = parseInt(document.getElementById('budgetFilter').value);

    let filteredNames = Object.keys(allCarsData).filter(name => {
        const car = allCarsData[name];
        const typeMatch = (selectedType === 'All' || car.type === selectedType);
        const budgetMatch = (car.price_num <= maxBudget);
        return typeMatch && budgetMatch;
    });

    if(filteredNames.length > 0) {
        populateDropdowns(filteredNames);
        loadComparison();
    } else {
        alert("No car matched this budget and type filter!");
    }
}

// Side-by-side comparison and loading live images for both cars
function loadComparison() {
    const car1 = document.getElementById('carSelect1')?.value;
    const car2 = document.getElementById('carSelect2')?.value;

    if(allCarsData[car1]) {
        const c1 = allCarsData[car1];
        if(document.getElementById('carTitle1')) {
            document.getElementById('carTitle1').innerText = car1;
            document.getElementById('brand1').innerText = c1.brand + ` (${c1.type})`;
            document.getElementById('price1').innerText = c1.price;
            document.getElementById('hpSpeed1').innerText = `${c1.hp} HP / ${c1.top_speed} km/h`;
            document.getElementById('extra1').innerText = `${c1.mileage_str} / ${c1.safety}`;
            document.getElementById('desc1').innerText = c1.desc;
            document.getElementById('carImg1').src = c1.img;
            document.getElementById('carImg1').style.display = 'block';
        }
    }

    if(allCarsData[car2]) {
        const c2 = allCarsData[car2];
        if(document.getElementById('carTitle2')) {
            document.getElementById('carTitle2').innerText = car2;
            document.getElementById('brand2').innerText = c2.brand + ` (${c2.type})`;
            document.getElementById('price2').innerText = c2.price;
            document.getElementById('hpSpeed2').innerText = `${c2.hp} HP / ${c2.top_speed} km/h`;
            document.getElementById('extra2').innerText = `${c2.mileage_str} / ${c2.safety}`;
            document.getElementById('desc2').innerText = c2.desc;
            document.getElementById('carImg2').src = c2.img;
            document.getElementById('carImg2').style.display = 'block';
        }
    }
}

// Logic to build an interactive bar chart using Chart.js
function buildChart() {
    const chartCanvas = document.getElementById('carChart');
    if(!chartCanvas) return;

    const ctx = chartCanvas.getContext('2d');
    const labels = Object.keys(allCarsData);
    const hpData = labels.map(name => allCarsData[name].hp);
    const mileageData = labels.map(name => allCarsData[name].mileage);

    if (myChart) myChart.destroy(); // Destroy old chart before re-rendering a new one

    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                { label: 'Horsepower (HP)', data: hpData, backgroundColor: '#e10600', borderWidth: 1 },
                { label: 'Mileage (kmpl)', data: mileageData, backgroundColor: '#ffeb3b', borderWidth: 1 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: '#333' }, ticks: { color: '#fff' } },
                x: { grid: { color: '#333' }, ticks: { color: '#fff' } }
            },
            plugins: { legend: { labels: { color: '#fff' } } }
        }
    });
}

// Logic to filter the car dropdown based on the selected company
function filterCarsByCompany() {
    const selectedCompany = document.getElementById('companySelect').value;
    const carSelect = document.getElementById('carSelect');
    
    // Clear the dropdown
    carSelect.innerHTML = '';

    // Pull only matching company cars from the entire database
    Object.keys(allCarsData).forEach(name => {
        const car = allCarsData[name];
        if (selectedCompany === 'All' || car.brand === selectedCompany) {
            const option = document.createElement('option');
            option.value = name;
            option.innerText = name;
            carSelect.appendChild(option);
        }
    });

    // Automatically load the first car's data based on the new list
    if (carSelect.options.length > 0) {
        loadCarData();
    }
}