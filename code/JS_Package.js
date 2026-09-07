
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


// --------------------------------------------------
// DISPLAY PROJECTS
// --------------------------------------------------

function renderProjects() {

    const projectList =
        document.getElementById("projectList");

    const filteredProjects =
        getFilteredProjects();

    const totalPages =
        Math.ceil(filteredProjects.length / projectsPerPage);

    // Make sure current page still exists
    if (currentPage > totalPages && totalPages > 0) {
        currentPage = totalPages;
    }

    const start =
        (currentPage - 1) * projectsPerPage;

    const end =
        start + projectsPerPage;

    const pageProjects =
        filteredProjects.slice(start, end);


    let html = `
        <table class="projectTable">
    `;


    pageProjects.forEach((project, index) => {

        // Alternate based on the actual position
        // on the current page.
        const imageLeft = index % 2 === 0;


        if (imageLeft) {

            html += `
                <tr>
                    <th>
                        <a href="${project.link}">
                            <img
                                class="imageCircle2 projectImage"
                                src="${project.icon}"
                                alt="${project.title}"
                            >
                        </a>
                    </th>

                    <th>
                        <a
                            class="projectTitle"
                            href="${project.link}"
                        >
                            ${project.title}
                        </a>

                        <p class="textInfo projectDescription">
                            ${project.description}
                        </p>
                    </th>
                </tr>
            `;

        } else {

            html += `
                <tr>
                    <th>
                        <a
                            class="projectTitle"
                            href="${project.link}"
                        >
                            ${project.title}
                        </a>

                        <p class="textInfo projectDescription">
                            ${project.description}
                        </p>
                    </th>

                    <th>
                        <a href="${project.link}">
                            <img
                                class="imageCircle2 projectImage"
                                src="${project.icon}"
                                alt="${project.title}"
                            >
                        </a>
                    </th>
                </tr>
            `;

        }

    });


    html += `</table>`;

    projectList.innerHTML = html;

    renderPagination(totalPages);

}


// --------------------------------------------------
// PAGINATION
// --------------------------------------------------

function renderPagination(totalPages) {

    const pagination =
        document.getElementById("pagination");

    pagination.innerHTML = "";

    if (totalPages <= 1) {
        return;
    }


    // Previous button

    if (currentPage > 1) {

        const previous =
            document.createElement("button");

        previous.textContent = "← Previous";

        previous.onclick = function() {
            currentPage--;
            renderProjects();
            window.scrollTo(0, 0);
        };

        pagination.appendChild(previous);

    }


    // Page numbers

    for (let page = 1; page <= totalPages; page++) {

        const button =
            document.createElement("button");

        button.textContent = page;

        if (page === currentPage) {
            button.classList.add("active");
        }

        button.onclick = function() {

            currentPage = page;

            renderProjects();

            window.scrollTo(0, 0);

        };

        pagination.appendChild(button);

    }


    // Next button

    if (currentPage < totalPages) {

        const next =
            document.createElement("button");

        next.textContent = "Next →";

        next.onclick = function() {

            currentPage++;

            renderProjects();

            window.scrollTo(0, 0);

        };

        pagination.appendChild(next);

    }

}


function createKeywordList() {

    const keywordDropdown = document.getElementById("keywordDropdown");

    const allKeywords = [
        ...new Set(
            projects.flatMap(project => project.keywords)
        )
    ];

    allKeywords.sort((a, b) => a.localeCompare(b));

    keywordDropdown.innerHTML = "";

    allKeywords.forEach(keyword => {

        const label = document.createElement("label");
        label.className = "keywordOption";

        const checkbox = document.createElement("input");

        checkbox.type = "checkbox";
        checkbox.value = keyword;

        checkbox.addEventListener("change", function() {

            if (this.checked) {
                selectedKeywords.push(keyword);
            } else {
                selectedKeywords =
                    selectedKeywords.filter(k => k !== keyword);
            }

            currentPage = 1;
            renderProjects();

        });

        label.appendChild(checkbox);
        label.appendChild(
            document.createTextNode(keyword)
        );

        keywordDropdown.appendChild(label);

    });

}


// --------------------------------------------------
// FILTER PROJECTS
// --------------------------------------------------

function getFilteredProjects() {

    if (selectedKeywords.length === 0) {
        return projects;
    }

    return projects.filter(project => {

        // OR filtering:
        // project appears if it contains ANY selected keyword

        return selectedKeywords.some(keyword =>
            project.keywords.includes(keyword)
        );

    });

}