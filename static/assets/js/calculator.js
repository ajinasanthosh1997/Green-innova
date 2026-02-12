/**
 * Solar Calculator Logic for Green Innova
 * Based on UAE solar parameters
 */

const SOLAR_PARAMS = {
    utilityRate: 0.30,           // AED per kWh (Approximate average)
    peakSunHours: 5.5,          // Average for UAE
    performanceRatio: 0.75,     // Efficiency factor (dust, temperature, inverter)
    panelWattage: 450,          // Watts per panel
    co2PerKwh: 0.5,             // kg of CO2 saved per kWh
    treesPerKgCo2: 0.05,        // Trees planted per kg CO2 saved
    annualDegradation: 0.005,   // 0.5% yearly loss in efficiency
    utilityInflation: 0.03      // 3% yearly electricity price increase
};

function calculateSolar(monthlyBill) {
    // Calibrate based on 700 AED reference: 11 kWp system, 63 Sqm area
    const scaleFactor = monthlyBill / 700;
    const systemSize = 11 * scaleFactor;
    const numPanels = Math.ceil((systemSize * 1000) / SOLAR_PARAMS.panelWattage);
    const areaRequired = 63 * scaleFactor;
    
    // Yearly data for basic metrics
    const yearlyProduction = systemSize * SOLAR_PARAMS.peakSunHours * 365 * SOLAR_PARAMS.performanceRatio;
    const yearlySavings = monthlyBill * 12 * 0.9; // Ballpark 90% offset
    const monthlySavings = yearlySavings / 12;

    const co2Saved = yearlyProduction * SOLAR_PARAMS.co2PerKwh;
    const treesPlanted = Math.round(co2Saved * SOLAR_PARAMS.treesPerKgCo2);
    
    // Projections logic (Calibrated to hit reference 20-yr savings at 700 AED)
    // Performance: 1,176 AED @ 700
    // Fixed: 954 AED @ 700
    // Lease: 15,378 AED @ 700
    const generatePlanData = (savingsAt700, upfront) => {
        const net20YearSavings = Math.round(savingsAt700 * scaleFactor);
        const planProjections = [];
        let cumulative = 0;
        const yearIncrement = net20YearSavings / 20;
        for (let year = 1; year <= 20; year++) {
            cumulative += yearIncrement;
            planProjections.push(Math.round(cumulative));
        }
        return {
            net20YearSavings,
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
            performance: generatePlanData(1176, 0),
            fixed: generatePlanData(954, 0),
            leaseToOwn: {
                ...generatePlanData(15378, 0),
                monthlyPayment: Math.round(997 * scaleFactor),
                leasePeriod: "60 Months",
                outOfPocket: "0 AED"
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
