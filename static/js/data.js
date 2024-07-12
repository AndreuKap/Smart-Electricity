// Функция группировки данных по периоду
function groupDataByPeriod(data, period) {
    if (period === 'day') {
        // Возвращаем последние 24 записи
        return data.slice(-24).map(record => ({
            date: record.datetime.toISOString().substring(0, 10),
            power: record.power
        }));
    }
    
    // Группировка данных для недели, месяца и года
    const groupedData = {};
    data.forEach(record => {
        let key;
        switch (period) {
            case 'week':
                // Группировка по дням для последних 14 дней
                key = record.datetime.toISOString().substring(0, 10); // YYYY-MM-DD
                break;
            case 'month':
                // Группировка по дням в текущем месяце
                key = record.datetime.toISOString().substring(0, 7); // YYYY-MM-DD
                break;
            case 'year':
                // Группировка по месяцам в текущем году
                key = record.datetime.toISOString().substring(0, 4); // YYYY-MM
                break;
        }

        if (!groupedData[key]) {
            groupedData[key] = {
                power: 0,
                count: 0
            };
        }

        groupedData[key].power += record.power;
        groupedData[key].count += 1;
    });

    // Преобразование объекта в массив
    return Object.entries(groupedData).map(([date, info]) => ({
        date,
        power: info.power
    }));
}

// Функция для получения даты начала последнего периода
function getLastPeriodStartDate(period) {
    const now = new Date();
    let startDate;

    switch (period) {
        case 'day':
            startDate = new Date(now.toISOString().substring(0, 10)); // Сегодня в полночь
            break;
        case 'week':
            startDate = new Date(now);
            startDate.setDate(now.getDate() - now.getDay()); // Начало текущей недели
            startDate.setHours(0, 0, 0, 0);
            break;
        case 'month':
            startDate = new Date(now.getFullYear(), now.getMonth(), 1); // Начало текущего месяца
            break;
        case 'year':
            startDate = new Date(now.getFullYear(), 0, 1); // Начало текущего года
            break;
    }

    return startDate;
}

// Функция для подсчета дневного и ночного потребления
function calculateDayNightConsumption(data) {
    let dayConsumption = 0;
    let nightConsumption = 0;

    data.forEach(record => {
        const hour = record.datetime.getHours();
        if (hour >= 7 && hour < 23) {
            dayConsumption += record.power;
        } else {
            nightConsumption += record.power;
        }
    });

    return { dayConsumption, nightConsumption };
}

// Функция группировки данных по дням и ночам
function groupDayNightData(data) {
    const dayData = [];
    const nightData = [];

    data.forEach(record => {
        const hour = record.datetime.getHours();
        if (hour >= 7 && hour < 23) {
            dayData.push(record);
        } else {
            nightData.push(record);
        }
    });

    return { dayData, nightData };
}

// Функция для фильтрации данных за последний период
function filterDataByLastPeriod(data, period) {
    const now = new Date();
    let startDate;

    switch (period) {
        case 'day':
            return data.slice(-24);
        case 'week':
            startDate = new Date();
            startDate.setDate(now.getDate() - 20); // 14 дней включая сегодня
            break;
        case 'month':
            startDate = new Date(now.getFullYear(), now.getMonth()-12, 1);
            break;
        case 'year':
            startDate = new Date(now.getFullYear()-10, 0, 1);
            break;
    }

    startDate.setHours(0, 0, 0, 0);
    return data.filter(record => record.datetime >= startDate);
}
// Функция для фильтрации данных за последний период (понедельно для круговой диаграммы)
function filterDataByLastetPeriod(data, period) {
    const now = new Date();
    let startDate;

    switch (period) {
        case 'day':
            return data.slice(-24);
        case 'week':
            startDate = new Date();
            startDate.setDate(now.getDate() - 7); 
            break;
        case 'month':
            startDate = new Date(now.getFullYear(), now.getMonth(), 1);
            break;
        case 'year':
            startDate = new Date(now.getFullYear(), 0, 1);
            break;
    }

    startDate.setHours(0, 0, 0, 0);
    return data.filter(record => record.datetime >= startDate);
}

function filterDataByPreLastetMonth(data) {
    const now = new Date();
    let startDate;

            startDate = new Date(now.getFullYear(), now.getMonth()-1, 1);
      
    startDate.setHours(0, 0, 0, 0);
    return data.filter(record => record.datetime >= startDate);
}


// Функция обновления линейного графика
function updateChart(period) {
    const filteredData = filterDataByLastPeriod(countersData, period);
    const groupedData = groupDataByPeriod(filteredData, period);

    consumptionChart.data.labels = groupedData.map(data => data.date);
    consumptionChart.data.datasets[0].data = groupedData.map(data => data.power);
    consumptionChart.update();
}
// Функция для подсчета дневного и ночного потребления
function calculateDayNightConsumption(data) {
    let dayConsumption = 0;
    let nightConsumption = 0;

    data.forEach(record => {
        const hour = record.datetime.getHours();
        if (hour >= 23 || hour < 7) {
            dayConsumption += record.power;
        } else {
            nightConsumption += record.power;
        }
    });

    return { dayConsumption, nightConsumption };
}

// Обновление накопительной гистограммы
function updateStackedChart(period) {
    if (period === 'day') {
       document.getElementById('stackedConsumptionChartContainer').style.display = 'none';
       return;
    }

    document.getElementById('stackedConsumptionChartContainer').style.display = 'block';

    const filteredData = filterDataByLastPeriod(countersData, period);
    const groupedData = groupDataByPeriod(filteredData, period);

    const dayData = [];
    const nightData = [];
    const labels = [];

    groupedData.forEach(group => {
        let dayPower = 0;
        let nightPower = 0;

        filteredData.forEach(record => {
            let recordKey;

            switch (period) {
                case 'week':
                    recordKey = record.datetime.toISOString().substring(0, 10); // YYYY-MM-DD
                    break;
                case 'month':
                    recordKey = record.datetime.toISOString().substring(0, 7); // YYYY-MM-DD
                    break;
                case 'year':
                    recordKey = record.datetime.toISOString().substring(0, 4); // YYYY-MM
                    break;
            }

            if (recordKey === group.date) {
                const hour = record.datetime.getHours();
                if (hour >= 7 && hour < 23) {
                    dayPower += record.power;
                } else {
                    nightPower += record.power;
                }
            }
        });

        dayData.push(dayPower);
        nightData.push(nightPower);
        labels.push(group.date);
    });

    stackedConsumptionChart.data.labels = labels;
    stackedConsumptionChart.data.datasets[0].data = dayData;
    stackedConsumptionChart.data.datasets[1].data = nightData;
    stackedConsumptionChart.update();
}


// Обновление графиков дневного и ночного потребления (требует исправления)
function updateDayNightLineCharts(period) {
    const filteredData = filterDataByLastPeriod(countersData, period);
    const groupedData = groupDataByPeriod(filteredData, period);

    const dayData = [];
    const nightData = [];

    groupedData.forEach(group => {
        let dayPower = 0;
        let nightPower = 0;
        let dayPower_m = [];

        // Фильтруем исходные данные по текущей дате в группе
        filteredData.forEach(record => {
            const recordDate = record.datetime.toISOString().substring(0, 10);
            const groupDate = group.date;

            if (period === 'year') {
                if (recordDate.substring(0, 4) === groupDate) {
                    // группируем по месяцам
                    const hour = record.datetime.getHours();
                    if (hour >= 7 && hour < 23) {
                        dayPower += record.power;
                    } else {
                        nightPower += record.power;
                    }
                }
            } else if (period === 'month') {
                if (recordDate.substring(0, 7) === groupDate) {
                    // группируем по месяцам
                    const hour = record.datetime.getHours();
                    if (hour >= 7 && hour < 23) {
                        dayPower += record.power;
                    } else {
                        nightPower += record.power;
                    }
                }
            
            } else if (period === 'week') {
                if (recordDate === groupDate) {
                    //неделя: группируем по дням
                    const hour = record.datetime.getHours();
                    if (hour >= 7 && hour < 23) {
                        dayPower += record.power;
                    } else {
                        nightPower += record.power;
                    }
                }
            } else if (period === 'day') {
                // День: используем последние 24 записи без дополнительной группировки
                const hour = record.datetime.getHours();
                if (hour >= 7 && hour < 23) {
                    dayPower_m = record.power;

                } else {
                    nightPower = record.power;
            
                }
            }
        });

        if (period === 'day') {
            dayData.push({ date: group.date, power: dayPower_m});
            console.log(dayData)
            nightData.push({ date: group.date, power: nightPower });
        } else {
            dayData.push({ date: group.date, power: dayPower });
            nightData.push({ date: group.date, power: nightPower });
        }
    });

    // Обновление дневного графика
    dayConsumptionChart.data.labels = dayData.map(data => data.date);
    dayConsumptionChart.data.datasets[0].data = dayData.map(data => data.power);
    dayConsumptionChart.update();

    // Обновление ночного графика
    nightConsumptionChart.data.labels = nightData.map(data => data.date);
    nightConsumptionChart.data.datasets[0].data = nightData.map(data => data.power);
    nightConsumptionChart.update();
}


// Обновление круговой диаграммы при изменении периода
function updateDayNightChart(period) {
    const filteredData = filterDataByLastetPeriod(countersData, period);
    const { dayConsumption, nightConsumption } = calculateDayNightConsumption(filteredData);
    dayNightChart.data.datasets[0].data = [nightConsumption, dayConsumption];
    datatable(dayConsumption, nightConsumption);
    dayNightChart.update();
}


// Обновление функции updateDayNightChart для обработки изменений
function updateDayNightChart(period) {
        const filteredData = filterDataByLastetPeriod(countersData, period);
        const { dayConsumption, nightConsumption } = calculateDayNightConsumption(filteredData);
        dayNightChart.data.datasets[0].data = [nightConsumption, dayConsumption];
        datatable(dayConsumption, nightConsumption);
        dayNightChart.update();
        Nero(summarizeDataByPeriodsNero(countersData, period));
    }

    function summarizeDataByPeriodsNero(data, period) {
        const now = new Date();
        const periodsToSummarize = 5;
        const summarizedData = [];
    
        for (let i = 0; i < periodsToSummarize; i++) {
            let startDate, endDate;
            let sum = 0;
    
            switch (period) {
                case 'day':
                    startDate = new Date(now);
                    startDate.setDate(now.getDate() - i);
                    startDate.setHours(0, 0, 0, 0);
                    endDate = new Date(startDate);
                    endDate.setDate(endDate.getDate() + 1);
                    break;
                case 'week':
                    startDate = new Date(now);
                    startDate.setDate(now.getDate() - 7 * i);
                    startDate.setHours(0, 0, 0, 0);
                    endDate = new Date(startDate);
                    endDate.setDate(endDate.getDate() + 7);
                    break;
                case 'month':
                    startDate = new Date(now.getFullYear(), now.getMonth() - i, 1);
                    endDate = new Date(startDate.getFullYear(), startDate.getMonth() + 1, 1);
                    break;
                case 'year':
                    startDate = new Date(now.getFullYear() - i, 0, 1);
                    endDate = new Date(startDate.getFullYear() + 1, 0, 1);
                    break;
            }
            const periodData = data.filter(record => {
                const recordDate = new Date(record.datetime);
                return recordDate >= startDate && recordDate < endDate;
            });
            sum = periodData.reduce((acc, record) => acc + record.power, 0);
    
            summarizedData.push(sum);
        }
    
        return summarizedData;
    }
    
    function Nero(summarizedData) {
        const url = '../analize/'; 
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', document.querySelector('meta[name="csrf-token"]').getAttribute('content'));
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    var response = JSON.parse(xhr.responseText);
                    console.log('Ответ от сервера:', response.value);
                    document.getElementById('nero_value').textContent = (parseFloat(response.value)*2.6).toFixed(2);
                } catch (e) {
                    console.error('Ошибка при парсинге ответа:', e);
                }
            } else {
                console.error('Ошибка при запросе. Код состояния:', xhr.status);
            }
        };
        xhr.onerror = function () {
            console.error('Ошибка соединения');
        };
    
        xhr.send(JSON.stringify(summarizedData));
    }
        
    
    
  





