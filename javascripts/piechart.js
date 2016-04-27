/*
 Example code for d3.js pie chart
 -----------------------------------
 height, width, divId and inputData would be inputs to a function
 -----------------------------------
 Owen Littlejohns 2016 April 26th
 */

var height    = 125;
var width     = 125;
var divId     = "#pieChartExample"
var inputData = [{"name": "Name 1", "value": 10}, {"name": "Name 2", "value": 7}, {"name": "Name 3", "value": 5}, {"name": "Name 4", "value": 2}, {"name": "Name 5", "value": 1}, {"name": "Name 6", "value": 1}]

var radius = Math.min(width, height) / 2;

// Create SVG element for pie chart, and add to the divId element

var svg = d3.select(divId)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('class', 'pieChart')
    .append('g')
    .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');

// Create tooltip and attach to the divId
var tooltip = d3.select(divId)
    .append('div')
    .attr('class', 'pieChartTooltip')
    .attr('position', 'absolute')
    .attr('z-index', '10')
    .style('display', 'none');

tooltip.append('div')
    .attr('class', 'tooltipKey')
    .attr('text-anchor', 'middle');

tooltip.append('div')
    .attr('class', 'tooltipValue')
    .attr('text-anchor', 'middle');

// Set the colour scheme using a d3 default:
var colour = d3.scale.category20c();

//Define default pie chart radii (make it a doughnut):
var arc = d3.svg.arc()
    .outerRadius(radius - 10)
    .innerRadius(radius - 20);

//Define radii for segment when mouse hovers over it:
var arcOver = d3.svg.arc()
    .outerRadius(radius)
    .innerRadius(radius - 15);

var labelArc = d3.svg.arc()
    .outerRadius(radius - 40)
    .innerRadius(radius - 40);

// Start and end of the segments
var pie = d3.layout.pie()
    .sort(null)
    .value(function(d) {return d["value"]; });

// Append the segments
var path = svg.selectAll('path')
    .data(pie(inputData))
    .enter()
    .append('path')
    .attr('d', arc)
    .attr('fill', function(d, i) {	return colour(i); } )
    .on('mouseover', function(d) {
	d3.select(this).transition()
	    .duration(1000)
	    .attr("d", arcOver);
	
	//tooltip.style('opacity', '1');
	tooltip.style('display', 'inline');
    })
    .on('mousemove', function(d) {

	var mouseCoords = d3.mouse(tooltip.node().parentElement);
	tooltip.select('.tooltipKey').text(d.data['name']);
	tooltip.select('tooltipValue').text(d.data['value']);
	tooltip.attr('transform', 'translate(' + (mouseCoords[0] - 10) 
		     + ',' + (mouseCoords[1] - 10) + ')');
	//tooltip.style('top', (event.pageY - 10) + 'px');
	//tooltip.style('left', (event.pageX + 10) + 'px');
    })
    .on('mouseout', function(d) {
	d3.select(this).transition()
	    .duration(1000)
	    .attr('d', arc);
	//tooltip.style('opacity', '0');
	tooltip.style('display', 'none');
    });
