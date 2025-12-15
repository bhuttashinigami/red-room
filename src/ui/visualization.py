def create_visualization_html(agent):
    """Generate complete HTML visualization for the traffic intersection."""
    state = {
        "traffic_counts": agent.traffic_counts,
        "current_green": agent.current_green,
        "green_timings": agent.green_timings,
        "high_traffic_road": agent.high_traffic_road,
    }

    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #1a1a2e;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;
}}
#intersection {{
    position: relative;
    width: 500px;
    height: 500px;
}}
.road {{
    position: absolute;
    background: #555;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.vertical {{
    width: 120px;
    height: 500px;
    left: 190px;
}}
.horizontal {{
    width: 500px;
    height: 120px;
    top: 190px;
}}
.center {{
    position: absolute;
    width: 120px;
    height: 120px;
    left: 190px;
    top: 190px;
    background: #333;
    border: 3px solid #666;
}}
.traffic-light {{
    position: absolute;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 2px solid #333;
}}
.red {{ background: #ff4444; }}
.green {{ background: #44ff44; box-shadow: 0 0 20px #44ff44; }}
.label {{
    position: absolute;
    font-size: 18px;
    font-weight: bold;
}}
.traffic-info {{
    position: absolute;
    background: rgba(0,0,0,0.7);
    padding: 8px;
    border-radius: 5px;
    font-size: 14px;
}}
.bar {{
    width: 140px;
    height: 12px;
    background: #222;
    border: 1px solid #555;
    margin-top: 4px;
}}
.bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, #4CAF50, #9cff57);
}}
.high-traffic {{
    color: #ff4444;
    font-weight: bold;
}}
</style>
</head>
<body>
<div id="intersection">
    <!-- Roads -->
    <div class="road vertical"></div>
    <div class="road horizontal"></div>
    <div class="center"></div>

    <!-- Traffic lights -->
    <div class="traffic-light {'green' if state['current_green']=='north' else 'red'}" style="left: 235px; top: 150px;"></div>
    <div class="traffic-light {'green' if state['current_green']=='south' else 'red'}" style="left: 235px; top: 320px;"></div>
    <div class="traffic-light {'green' if state['current_green']=='east' else 'red'}" style="left: 320px; top: 235px;"></div>
    <div class="traffic-light {'green' if state['current_green']=='west' else 'red'}" style="left: 150px; top: 235px;"></div>

    <!-- Labels -->
    <div class="label" style="left: 230px; top: 20px;">NORTH</div>
    <div class="label" style="left: 230px; top: 460px;">SOUTH</div>
    <div class="label" style="left: 420px; top: 235px;">EAST</div>
    <div class="label" style="left: 30px; top: 235px;">WEST</div>

    <!-- Traffic Info -->
    <!-- NORTH -->
    <div class="traffic-info" style="left: 180px; top: 70px;">
        <div><strong>NORTH</strong>{'<span class="high-traffic"> (HIGH)</span>' if state['high_traffic_road']=='north' else ''}</div>
        <div>Cars: {state['traffic_counts']['north']}</div>
        <div>Current: {state['green_timings']['north']['current']}s</div>
        <div>Last: {state['green_timings']['north']['last']}s</div>
        <div class="bar"><div class="bar-fill" style="width: {min(state['traffic_counts']['north']*4,140)}px;"></div></div>
    </div>
    <!-- SOUTH -->
    <div class="traffic-info" style="left: 180px; top: 380px;">
        <div><strong>SOUTH</strong>{'<span class="high-traffic"> (HIGH)</span>' if state['high_traffic_road']=='south' else ''}</div>
        <div>Cars: {state['traffic_counts']['south']}</div>
        <div>Current: {state['green_timings']['south']['current']}s</div>
        <div>Last: {state['green_timings']['south']['last']}s</div>
        <div class="bar"><div class="bar-fill" style="width: {min(state['traffic_counts']['south']*4,140)}px;"></div></div>
    </div>
    <!-- EAST -->
    <div class="traffic-info" style="left: 350px; top: 200px;">
        <div><strong>EAST</strong>{'<span class="high-traffic"> (HIGH)</span>' if state['high_traffic_road']=='east' else ''}</div>
        <div>Cars: {state['traffic_counts']['east']}</div>
        <div>Current: {state['green_timings']['east']['current']}s</div>
        <div>Last: {state['green_timings']['east']['last']}s</div>
        <div class="bar"><div class="bar-fill" style="width: {min(state['traffic_counts']['east']*4,140)}px;"></div></div>
    </div>
    <!-- WEST -->
    <div class="traffic-info" style="left: 50px; top: 200px;">
        <div><strong>WEST</strong>{'<span class="high-traffic"> (HIGH)</span>' if state['high_traffic_road']=='west' else ''}</div>
        <div>Cars: {state['traffic_counts']['west']}</div>
        <div>Current: {state['green_timings']['west']['current']}s</div>
        <div>Last: {state['green_timings']['west']['last']}s</div>
        <div class="bar"><div class="bar-fill" style="width: {min(state['traffic_counts']['west']*4,140)}px;"></div></div>
    </div>
</div>
</body>
</html>
"""
    return html
