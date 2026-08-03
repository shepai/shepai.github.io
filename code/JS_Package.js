
function load_3d(){
for(let i=0; i<stlFiles.length; i++){

    createSTLViewer(
        containers[i],
        stlFiles[i]
    );

}
}


function createSTLViewer(containerID, url){


    let container = document.getElementById(containerID);

	let mesh = null;
    // Scene
    let scene = new THREE.Scene();



    // Camera
    let camera = new THREE.PerspectiveCamera(
        45,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );


    camera.position.set(
        0,
        0,
        100
    );



    // Renderer
    let renderer = new THREE.WebGLRenderer({
        antialias:true,
        alpha:true
    });


    renderer.setSize(
        container.clientWidth,
        container.clientHeight
    );


    container.innerHTML = "";
    container.appendChild(
        renderer.domElement
    );



    // Lighting

    let light = new THREE.DirectionalLight(
        0xffffff,
        2
    );


    light.position.set(
        1,
        1,
        1
    );


    scene.add(light);


    scene.add(
        new THREE.AmbientLight(
            0xffffff,
            0.8
        )
    );



    // Loading text

    let loadingText = document.createElement("p");

    loadingText.innerHTML = "Loading STL...";

    container.appendChild(
        loadingText
    );



    // STL loader

    let loader = new THREE.STLLoader();



    loader.load(

        url,


        function(geometry){


            console.log(
                "Loaded:",
                url
            );


            loadingText.remove();



            geometry.computeBoundingBox();

            geometry.center();



            let material = new THREE.MeshPhongMaterial({

                color:0x888888

            });



            mesh = new THREE.Mesh(
				geometry,
				material
			);


            scene.add(mesh);
			mesh.rotation.x = -Math.PI / 4;
			mesh.rotation.z = Math.PI / 6;


            // Scale model

            let size = geometry.boundingBox.getSize(

                new THREE.Vector3()

            );


            let maxDim = Math.max(

                size.x,

                size.y,

                size.z

            );


            let scale = 30 / maxDim;

mesh.scale.setScalar(scale);


// move camera automatically
camera.position.set(
    0,
    0,
    100
);

camera.lookAt(
    0,
    0,
    0
);



        },



        function(xhr){


            if(xhr.total > 0){

                let percent = (

                    xhr.loaded / xhr.total * 100

                ).toFixed(0);



                loadingText.innerHTML =

                    "Loading STL: " + percent + "%";

            }


        },



        function(error){


            console.error(

                "Failed loading:",

                url,

                error

            );


            loadingText.innerHTML =
                "Failed to load STL";


        }


    );



    // Animation loop

   function animate(){

    requestAnimationFrame(animate);

    if(mesh){

        mesh.rotation.z += 0.005;

    }

    renderer.render(
        scene,
        camera
    );

}

animate();


}



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

window.onload = function(){

    let toc = document.getElementById("table-of-contents");

    let headings = document.querySelectorAll("h2, h3, h4");

    let rootList = document.createElement("ul");

    let currentLists = {
        2: rootList
    };

    headings.forEach(function(heading, index){

        // Create an ID if it does not already exist
        if(!heading.id){
            heading.id = "section-" + index;
        }

        let level = Number(heading.tagName.substring(1));

        let item = document.createElement("li");

        let link = document.createElement("a");

        link.href = "#" + heading.id;
        link.textContent = heading.textContent;

        item.appendChild(link);


        // If this is a main section
        if(level === 2){

            rootList.appendChild(item);

            currentLists[2] = rootList;

        }


        // If this is a subsection
        else if(level === 3){

            if(!currentLists[2].lastElementChild){
                return;
            }

            let subList = document.createElement("ul");

            subList.appendChild(item);

            currentLists[2]
                .lastElementChild
                .appendChild(subList);

            currentLists[3] = subList;

        }


        // If this is a sub-subsection
        else if(level === 4){

            if(!currentLists[3]){
                return;
            }

            let subSubList = document.createElement("ul");

            subSubList.appendChild(item);

            currentLists[3]
                .lastElementChild
                .appendChild(subSubList);

            currentLists[4] = subSubList;

        }

    });


    toc.appendChild(rootList);

}
