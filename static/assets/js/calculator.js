/**
 * Solar Calculator Logic for Green Innova
 * Based on UAE solar parameters
 */

const SOLAR_PARAMS = {
    utilityRate: 0.032,           // BHD per kWh (Approximate average)
    peakSunHours: 5.5,          // Average for UAE (Keeping same sun hours)
    performanceRatio: 0.75,     // Efficiency factor (dust, temperature, inverter)
    panelWattage: 450,          // Watts per panel
    co2PerKwh: 0.5,             // kg of CO2 saved per kWh
    treesPerKgCo2: 0.05,        // Trees planted per kg CO2 saved
    annualDegradation: 0.005,   // 0.5% yearly loss in efficiency
    utilityInflation: 0.03      // 3% yearly electricity price increase
};

function calculateSolar(monthlyBill) {
    // Calibrate based on 70 BHD reference: 11 kWp system, 63 Sqm area
    const scaleFactor = monthlyBill / 70;
    const systemSize = 11 * scaleFactor;
    const numPanels = Math.ceil((systemSize * 1000) / SOLAR_PARAMS.panelWattage);
    const areaRequired = 63 * scaleFactor;
    
    // Yearly data for basic metrics
    const yearlyProduction = systemSize * SOLAR_PARAMS.peakSunHours * 365 * SOLAR_PARAMS.performanceRatio;
    const yearlySavings = monthlyBill * 12 * 0.9; // Ballpark 90% offset
    const monthlySavings = yearlySavings / 12;

    const co2Saved = yearlyProduction * SOLAR_PARAMS.co2PerKwh;
    const treesPlanted = Math.round(co2Saved * SOLAR_PARAMS.treesPerKgCo2);
    
    // Projections logic (Calibrated to hit reference 20-yr savings at 70 BHD)
    // Performance: 117.6 BHD @ 70
    // Fixed: 95.4 BHD @ 70
    // Lease: 1537.8 BHD @ 70
    const generatePlanData = (savingsAt70, upfront) => {
        const net25YearSavings = Math.round(savingsAt70 * scaleFactor * (25 / 20)); // Adjusted for extra 5 years
        const planProjections = [];
        let cumulative = 0;
        const yearIncrement = net25YearSavings / 25;
        for (let year = 1; year <= 25; year++) {
            cumulative += yearIncrement;
            planProjections.push(Math.round(cumulative));
        }
        return {
            net25YearSavings,
            outOfPocket: upfront,
            payback: upfront > 0 ? "5.2 Years" : "Immediate",
            projections: planProjections
        };
    };

    return {
        monthlyBill,
        systemSize: systemSize.toFixed(1),
        numPanels,
        yearlyProduction: Math.round(yearlyProduction),
        yearlySavings: Math.round(yearlySavings),
        monthlySavings: Math.round(monthlySavings),
        co2Saved: Math.round(co2Saved),
        treesPlanted,
        roiPeriod: "5.4",
        areaRequired: Math.round(areaRequired),
        propertyValueIncrease: Math.round(systemSize * 3500 * 0.1),
        plans: {
            performance: generatePlanData(120, 0),
            fixed: generatePlanData(95, 0),
            leaseToOwn: {
                ...generatePlanData(1500, 0),
                monthlyPayment: Math.round(100 * scaleFactor),
                leasePeriod: "60 Months",
                outOfPocket: "0 BHD"
            }
        },
        technicalSpecs: {
            panelType: "Monocrystalline Perc",
            inverterEfficiency: "98.2%",
            mountingSystem: "Aluminum Rail (Roof)",
            monitoring: "Cloud-based WiFi App"
        }
    };
}

window.SolarCalculator = { calculateSolar };
