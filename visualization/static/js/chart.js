function map(data) {
    entries = { 'apple': [], 'amazon': [], 'facebook': [], 'google': [], 'microsoft': [] };
    var ap_i = 0;
    var am_i = 0;
    var fa_i = 0;
    var go_i = 0;
    var mi_i = 0;

    for (let i = 0; i < data.length; i++) {
        if (data[i]['Category'] == "Entry") {
            var rad = 5;
        }
        else if (data[i]['Category'] == "Mid") {
            var rad = 9;
        }
        else if (data[i]['Category'] == "Senior") {
            var rad = 15;
        }
        var yoe = data[i]['yearsofexperience'];
        var tyc = data[i]['totalyearlycompensation'];

        company_metrics = { 'x': yoe, 'y': tyc, 'r': rad };

        if (data[i]['company'] === "Apple") {
            entries.apple[ap_i] = company_metrics;
            ap_i++;
        } else if (data[i]['company'] === "Amazon") {
            entries.amazon[am_i] = company_metrics;
            am_i++;
        } else if (data[i]['company'] === "Facebook") {
            entries.facebook[fa_i] = company_metrics;
            fa_i++;
        } else if (data[i]['company'] === "Google") {
            entries.google[go_i] = company_metrics;
            go_i++;
        } else if (data[i]['company'] === "Microsoft") {
            entries.microsoft[mi_i] = company_metrics;
            mi_i++;
        } else {
            console.log('no company name');
        }
    }

    const mappedData = {
        datasets: [{
            label: "Apple",
            data: entries.apple,
            backgroundColor: "rgb(19,128,205,0.5)",
            hoverBorderColor: "rgb(110,148,175)",
            hoverBorderWidth: "4"
        }, {
            label: "Amazon",
            data: entries.amazon,
            backgroundColor: "rgb(205,19,168,0.5)",
            hoverBorderColor: "rgb(110,148,175)",
            hoverBorderWidth: "4"
        }, {
            label: "Facebook",
            data: entries.facebook,
            backgroundColor: "rgb(205,168,19,0.5)",
            hoverBorderColor: "rgb(110,148,175)",
            hoverBorderWidth: "4"
        }, {
            label: "Google",
            data: entries.amazon,
            backgroundColor: "rgb(205,44,19,0.5)",
            hoverBorderColor: "rgb(110,148,175)",
            hoverBorderWidth: "4"
        }, {
            label: "Microsoft",
            data: entries.microsoft,
            backgroundColor: "rgb(19,205,159,0.5)",
            hoverBorderColor: "rgb(110,148,175)",
            hoverBorderWidth: "4"
        },
        ]
    };

    const footer = (tooltipItems) => {
        var level;
        var salary;
        var yoe;
        tooltipItems.forEach(function(tooltipItem) {
            if (tooltipItem.parsed.r == 15) {
                level = "Senior";
            } else if (tooltipItem.parsed.r == 9) {
                level = "Mid";
            } else if (tooltipItem.parsed.r == 5) {
                level = "Entry";
            };
            salary = tooltipItem.parsed.y *1000;
            yoe = tooltipItem.parsed.x;
        })
        return 'Salary: $' + salary + '\nYears of Exp: ' + yoe
    }

    const config = {
        type: 'bubble',
        data: mappedData,
        options: {
            layout: {
                padding: 20
            },
            plugins: {
                title: {
                    display: true,
                    text: "Salaries by Experience and Company"
                },
                tooltip:{
                    callbacks: {
                        footer: footer
                    }
                }
            },
            scales: {
                xAxis: {
                    title: {
                        display: true,
                        text: "Years of Experience"
                    }
                },
                yAxis: {
                    title: {
                        display: true,
                        text: "Salary in $1,000"
                    }
                }
            }
        }
    };

    const myChart = new Chart(
        document.getElementById('chart'),
        config);
    
    
}

map(data);