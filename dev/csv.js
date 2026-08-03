function loadCSV(url){

    return new Promise((resolve) => {

        Papa.parse(url, {
            download: true,
            header: true,

            complete: function(results){

                let data = results.data;

                let markerColumns = Object.keys(data[0])
                    .filter(col => col.includes("marker"));

                let markerIDs = [...new Set(
                    markerColumns.map(col => {
                        return col.match(/marker_(\d+)/)[1];
                    })
                )];

                markerIDs.sort((a,b)=>a-b);


                let samples = data.map(row => {

                    let markers = [];

                    markerIDs.forEach(id => {

                        markers.push([
                            Number(row[`marker_${id}_x`]),
                            Number(row[`marker_${id}_y`]),
                            Number(row[`marker_${id}_z`])
                        ]);

                    });

                    return markers;

                });

                resolve(samples);

            }

        });

    });

}
const plots = {};

function createPlot(plotName, divId = "plot") {

    // If plot already exists, reset it
    if (plots[plotName]) {
        Plotly.purge(plots[plotName].divId);
    }

    plots[plotName] = {
        divId: divId,
        traces: []
    };

    Plotly.newPlot(
        divId,
        [],
        {
            margin: {
                l: 0,
                r: 0,
                t: 0,
                b: 0
            },
            paper_bgcolor: "rgba(0,0,0,0)",
            scene: {
                bgcolor: "rgba(0,0,0,0)",
                aspectmode: "data"
            }
        }
    );
}


function addMarkers(plotName, points, colour = "red") {

    let plot = plots[plotName];

    if (!plot) {
        console.error("Plot does not exist:", plotName);
        return;
    }

    let trace = {
        x: points.map(p => p[0]),
        y: points.map(p => p[1]),
        z: points.map(p => p[2]),

        mode: "markers",

        marker: {
            size: 5,
            color: colour
        },

        type: "scatter3d",

        name: "Points " + (plot.traces.length + 1)
    };

    plot.traces.push(trace);

    Plotly.addTraces(
        plot.divId,
        trace
    );
}