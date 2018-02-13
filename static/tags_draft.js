
var scaleRadius = d3.scaleLinear().domain([d3.min(data, function(d) {
            return +d[columnForRadius];
        }), d3.max(data, function(d) {
            return +d[columnForRadius];
        })]).range([5, 18])
var colorCircles = d3.scaleOrdinal(d3.schemeCategory10);

// var svg = div.selectAll('svg');

var node = d3.selectAll("g.node")
            .data(data)
            .enter()
            .attr('class', 'node')

    node.append("circle")
        .attr('r', function(d){
          return scaleRadius(d['count'])
        })
        .attr('fill', function(d){
          return colorCircles(d['user'])
        })
        
    node.append("text")
        // .attr('class', 'text')
        .attr('text', function(d) {
          return d.word
        })
        