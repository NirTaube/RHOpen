// Function to initialize the page
function init() {
    // Select the dropdown menu
    var dropdown = d3.select("#selDataset");
  
    // Read the samples.json data from the URL
    d3.json("samples.json").then(function(data) {
      // Get the sample names and populate the dropdown
      var sampleNames = data.names;
      sampleNames.forEach(function(sample) {
        dropdown.append("option")
          .text(sample)
          .property("value", sample);
      });
  
      // Get the first sample's data and update the charts, metadata, and gauge
      var firstSample = sampleNames[0];
      updateCharts(firstSample, data);
      updateMetadata(firstSample, data);
      updateGauge(firstSample, data);
    });
  }
  
  // Function to update the charts based on the selected sample
  function updateCharts(sample, data) {
    // Find the selected sample's data
    var selectedSample = data.samples.find(function(obj) {
      return obj.id === sample;
    });
  
    // Get the necessary arrays from the selected sample's data
    var sampleValues = selectedSample.sample_values.slice(0, 10).reverse();
    var otuIDs = selectedSample.otu_ids.slice(0, 10).reverse().map(id => `OTU ${id}`);
    var otuLabels = selectedSample.otu_labels.slice(0, 10).reverse();
  
    // Update the horizontal bar chart
    var barTrace = {
      x: sampleValues,
      y: otuIDs,
      text: otuLabels,
      type: "bar",
      orientation: "h"
    };
  
    var barData = [barTrace];
  
    var barLayout = {
      title: "Top 10 OTUs",
      margin: { t: 30, l: 150 }
    };
  
    Plotly.newPlot("bar", barData, barLayout);
  
    // Update the bubble chart
    var bubbleTrace = {
      x: selectedSample.otu_ids,
      y: selectedSample.sample_values,
      text: selectedSample.otu_labels,
      mode: "markers",
      marker: {
        size: selectedSample.sample_values,
        color: selectedSample.otu_ids,
        colorscale: "Earth"
      }
    };
  
    var bubbleData = [bubbleTrace];
  
    var bubbleLayout = {
      title: "OTU ID vs Sample Values",
      xaxis: { title: "OTU ID" },
      yaxis: { title: "Sample Values" },
      showlegend: false
    };
  
    Plotly.newPlot("bubble", bubbleData, bubbleLayout);
  }
  
  // Function to update the sample metadata
  function updateMetadata(sample, data) {
    // Find the selected sample's metadata
    var metadata = data.metadata.find(function(obj) {
      return obj.id.toString() === sample;
    });
  
    // Select the metadata panel and clear the existing content
    var metadataPanel = d3.select("#metadata");
    metadataPanel.html("");
  
    // Display each key-value pair from the metadata JSON object
    Object.entries(metadata).forEach(function([key, value]) {
      metadataPanel.append("p")
        .text(`${key}: ${value}`);
    });
  }
  
  // Function to update the Gauge Chart
  function updateGauge(sample, data) {
    // Find the selected sample's metadata
    var metadata = data.metadata.find(function(obj) {
      return obj.id.toString() === sample;
    });
  
    // Get the washing frequency value
    var washingFrequency = metadata.wfreq;
  
    // Update the Gauge Chart
    var gaugeData = [
      {
        domain: { x: [0, 1], y: [0, 1] },
        value: washingFrequency,
        title: { text: "Weekly Washing Frequency" },
        type: "indicator",
        mode: "gauge+number",
        gauge: {
          axis: { range: [null, 9] },
          steps: [
            { range: [0, 1], color: "#f5f5f5" },
            { range: [1, 2], color: "#e0e0e0" },
            { range: [2, 3], color: "#c7c7c7" },
            { range: [3, 4], color: "#aeaeae" },
            { range: [4, 5], color: "#949494" },
            { range: [5, 6], color: "#7b7b7b" },
            { range: [6, 7], color: "#626262" },
            { range: [7, 8], color: "#484848" },
            { range: [8, 9], color: "#2f2f2f" }
          ],
          threshold: {
            line: { color: "red", width: 4 },
            thickness: 0.75,
            value: washingFrequency
          }
        }
      }
    ];
  
    var gaugeLayout = { width: 500, height: 400, margin: { t: 0, b: 0 } };
  
    Plotly.newPlot("gauge", gaugeData, gaugeLayout);
  }
  
  // Function to handle the change event of the dropdown menu
  function optionChanged(sample) {
    // Read the samples.json data from the URL
    d3.json("samples.json").then(function(data) {
      // Update the charts, metadata, and gauge based on the selected sample
      updateCharts(sample, data);
      updateMetadata(sample, data);
      updateGauge(sample, data);
    });
  }

  //sample data card
  // Function to update the sample metadata
function updateMetadata(sample, data) {
    // Find the selected sample's metadata
    var metadata = data.metadata.find(function(obj) {
      return obj.id.toString() === sample;
    });
  
    // Select the metadata panel and clear the existing content
    var metadataPanel = d3.select("#sample-metadata");
    metadataPanel.html("");
  
    // Display each key-value pair from the metadata JSON object
    Object.entries(metadata).forEach(function([key, value]) {
      metadataPanel.append("p")
        .text(`${key}: ${value}`);
    });
  }
  
  
  // Initialize the page
  init();
    