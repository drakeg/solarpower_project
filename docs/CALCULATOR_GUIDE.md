# Solar calculator guide: methods, units, and limitations

These calculators are **planning estimates**, not electrical designs or equipment recommendations. Confirm all equipment ratings, wiring, protective devices, and installation requirements with manufacturer documentation and a qualified installer.

## Start with daily loads

**Daily Load Estimator:** daily energy (Wh/day) = running power (W) × quantity × hours operated per day. Divide Wh by 1,000 for kWh. Use measured average power for cycling appliances where possible; nameplate maximum wattage can overestimate actual daily consumption.

**Daily Load Worksheet:** sums the same calculation for up to 20 appliance rows. The link to System Sizing passes the total in **Wh/day**, not kWh/day. A load running for zero hours contributes zero Wh. Include all loads, including standby devices, chargers, and seasonal appliances. Do not confuse power (W) with energy (Wh).

## Size the array and battery

**Solar System Sizing** uses the following equations:

- Array power (W) = daily demand (Wh/day) ÷ peak sun hours (h/day) ÷ system efficiency fraction.
- Usable battery energy (Wh) = daily demand (Wh/day) × autonomy days.
- Nominal battery energy (Wh) = usable battery energy ÷ usable capacity fraction.
- Nominal battery capacity (Ah) = nominal battery energy (Wh) ÷ battery-bank voltage (V).

For example, 2,000 Wh/day, 4 peak sun hours, 80% system efficiency, 2 autonomy days, 80% usable battery capacity, and a 12 V bank yield a **625 W array**, **4,000 Wh usable storage**, **5,000 Wh nominal storage**, and **416.7 Ah nominal at 12 V**. These are mathematical minimum estimates, not rounded commercial equipment sizes.

Peak sun hours are *equivalent full-power sunlight*, not hours between sunrise and sunset. Use conservative, location- and season-specific values. The overall efficiency factor applies to **solar production**, not a second time to battery storage. Battery usable percentage represents the share of nominal energy you intend to discharge. Zero autonomy means **no battery storage is requested**, not that the system can operate without energy storage under every condition.

This model does not automatically account for shading, orientation, snow, extreme temperatures, cloudy-day sequences, battery charging limits, battery/inverter conversion losses outside the chosen assumptions, degradation, or equipment sizing increments. Ensure loads and efficiencies are defined consistently to avoid counting losses twice or omitting them.

## Size an inverter

**Inverter Sizing** uses the maximum *simultaneous* running AC load, not the sum of all appliances that might be used during a day:

- Recommended continuous output (W) = simultaneous running watts × (1 + headroom percentage / 100).
- Minimum surge output (W) = max(simultaneous running watts, simultaneous running watts − starting device running watts + largest starting watts).

If the starting device's running watts are omitted, the calculation conservatively adds its full starting watts to the other simultaneous load estimate. Starting-device running watts must not exceed total running watts; starting watts must not be lower than that device's running watts.

The surge estimate assumes **one largest starting event at a time**. It does not model simultaneous motor starts, surge *duration*, inverter waveform, derating, battery discharge limits, or manufacturer-specific overload behavior. Check both continuous and surge ratings and their specified durations.

## Understand solar savings

**Solar Savings** uses only the entered monthly bill, up-front system cost, and lifetime:

- Annual utility spending = monthly bill × 12.
- Annualized system cost = system cost ÷ lifetime years.
- Annual net savings = annual utility spending − annualized system cost.
- Lifetime net savings = (annual utility spending × lifetime years) − system cost.

It implicitly compares the full current bill against system cost and **does not estimate actual energy generation or bill offset**. It does not include export credits, grid fees, financing, incentives, maintenance, replacements, electricity inflation, panel degradation, or discounted cash flows. Treat it as a simple cost illustration, **not a payback or return-on-investment forecast**.

## Before buying equipment

Measure actual daily energy use and simultaneous startup demand, check your site's worst-season solar resource, choose realistic usable battery capacity and efficiency assumptions, and verify your equipment's electrical ratings and safety requirements. Re-run calculations with less favorable inputs to understand how much the estimate changes.
