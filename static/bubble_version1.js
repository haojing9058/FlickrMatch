function bubbleChart() {
    var width = 960,
        height = 960,
        maxRadius = 12,
        padding = 1.5
        clusterPadding = 6,
        // columnForColors = "user",
        // columnForRadius = "count",
        n = 60, // total number of circles
        m = 3; // number of distinct clusters
    var color = d3.scale.category10().domain(d3.range(m));
    // var colorCircles = d3.scaleOrdinal(d3.schemeCategory10);
    
    function chart(selection) {
        // var data = selection.enter().data();
        // var div = selection,
        //     svg = div.selectAll('svg');
        // svg.attr('width', width).attr('height', height);

        var cs = [];
        data.forEach(function(d){
                if(!cs.contains(d.group)) {
                    cs.push(d.group);
                }
        });//unique cluster/group id's

        var clusters = new Array(m);
        var nodes = [];
        for (var i = 0; i<n; i++){
            nodes.push(create_nodes(data,i));
        }

        var force = d3.layout.force()
            .nodes(nodes)
            .size([width, height])
            .gravity(.02)
            .charge(0)
            .on("tick", tick)
            .start();

        var svg = d3.select("body").append("svg")
            .attr("width", width)
            .attr("height", height);

        var node = svg.selectAll("circle")
            .data(nodes)
            .enter().append("g").call(force.drag);

        node.append("circle")
            .style("fill", function (d) {
            return color(d.cluster);
            })
            .attr("r", function(d){return d.radius})

        node.append("text")
          .attr("dy", ".3em")
          .style("text-anchor", "middle")
          .text(function(d) { return d.text.substring(0, d.radius / 3); });


        function create_nodes(data,node_counter) {
          var i = cs.indexOf(data[node_counter].group),
              r = Math.sqrt((i + 1) / m * -Math.log(Math.random())) * maxRadius,
              d = {
                cluster: i,
                radius: data[node_counter].size*1.5,
                text: data[node_counter].text,
                x: Math.cos(i / m * 2 * Math.PI) * 200 + width / 2 + Math.random(),
                y: Math.sin(i / m * 2 * Math.PI) * 200 + height / 2 + Math.random()
              };
          if (!clusters[i] || (r > clusters[i].radius)) clusters[i] = d;
          return d;
        };


        function tick(e) {
            node.each(cluster(10 * e.alpha * e.alpha))
                .each(collide(.5))
            .attr("transform", function (d) {
                var k = "translate(" + d.x + "," + d.y + ")";
                return k;
            })
        }

  // function ticked(e) {
  //           circles.attr("cx", function(d) {
  //                   return d.x;
  //               })
  //               .attr("cy", function(d) {
  //                   return d.y;
  //               });

  //           labels.attr("x", function(d) {
  //                   return d.x;
  //               })
  //                   .attr("y", function(d) {
  //                   return d.y;
  //               })
  //       }

// Move d to be adjacent to the cluster node.
        function cluster(alpha) {
            return function (d) {
                var cluster = clusters[d.cluster];
                if (cluster === d) return;
                var x = d.x - cluster.x,
                    y = d.y - cluster.y,
                    l = Math.sqrt(x * x + y * y),
                    r = d.radius + cluster.radius;
                if (l != r) {
                    l = (l - r) / l * alpha;
                    d.x -= x *= l;
                    d.y -= y *= l;
                    cluster.x += x;
                    cluster.y += y;
                }
            };
        }

// Resolves collisions between d and all other circles.
        function collide(alpha) {
            var quadtree = d3.geom.quadtree(nodes);
            return function (d) {
                var r = d.radius + maxRadius + Math.max(padding, clusterPadding),
                    nx1 = d.x - r,
                    nx2 = d.x + r,
                    ny1 = d.y - r,
                    ny2 = d.y + r;
                quadtree.visit(function (quad, x1, y1, x2, y2) {
                    if (quad.point && (quad.point !== d)) {
                        var x = d.x - quad.point.x,
                            y = d.y - quad.point.y,
                            l = Math.sqrt(x * x + y * y),
                            r = d.radius + quad.point.radius + (d.cluster === quad.point.cluster ? padding : clusterPadding);
                        if (l < r) {
                            l = (l - r) / l * alpha;
                            d.x -= x *= l;
                            d.y -= y *= l;
                            quad.point.x += x;
                            quad.point.y += y;
                        }
                    }
                    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
                });
            };
        }


        // var tooltip = selection
        //     .append("div")
        //     .style("position", "absolute")
        //     .style("visibility", "hidden")
        //     .style("color", "white")
        //     .style("padding", "8px")
        //     .style("background-color", "#626D71")
        //     .style("border-radius", "6px")
        //     .style("text-align", "center")
        //     .style("font-family", "monospace")
        //     .style("width", "400px")
        //     .text("");


        // var forced = d3.forceSimulation(data)
        //     .force("charge", d3.forceManyBody().strength([-99. -99]))
        //     .force("x", d3.forceX())
        //     .force("y", d3.forceY())
        //     .on("tick", ticked);

      


        // var scaleRadius = d3.scaleLinear().domain([d3.min(data, function(d) {
        //     return +d[columnForRadius];
        // }), d3.max(data, function(d) {
        //     return +d[columnForRadius];
        // })]).range([15, 28])

        // var nodes = svg.selectAll("circle")
        //     .data(data)
        //     .enter();

        // var circles = nodes.append("circle")
        //             .attr('r', function(d) { return scaleRadius(d[columnForRadius]) })
        //             .style("fill", function(d) { return colorCircles(d[columnForColors]) })
        //             .attr('transform', 'translate(' + [width / 2, height / 2] + ')')
        
        // var labels = nodes.append('text')  
        //     // .attr("x", function(d){ return d.x; })
        //     // .attr("y", function(d){ return d.y ; })
        //     .attr("text-anchor", "middle")
        //     .text(function(d){ return d.word;} )
        //     .style("fill","black")
        //     .style("font-family","Helvetica Neue, Helvetica, Arial, san-serif")
        //     .style("font-size", "10px")
        //     .attr('transform', 'translate(' + [width / 2, height / 2] + ')')
        //     .on("mouseover", function(d) {
        //         tooltip.html(d[columnForColors] + "<br>" + d.word + "<br>" + d[columnForRadius] + " hearts");
        //         return tooltip.style("visibility", "visible");
        //     })
        //     .on("mousemove", function() {
        //         return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px");
        //     })
        //     .on("mouseout", function() {
        //         return tooltip.style("visibility", "hidden");
        //     });
        // var node = svg.selectAll("circle")
        //     .data(data)
        //     .enter()
        //     .append("circle")
        //     .attr('r', function(d) {
        //         return scaleRadius(d[columnForRadius])
        //     })
        //     .style("fill", function(d) {
        //         return colorCircles(d[columnForColors])
        //     })
        //     .attr('transform', 'translate(' + [width / 2, height / 2] + ')')

    chart.width = function(value) {
        if (!arguments.length) {
            return width;
        }
        width = value;
        return chart;
    };

    chart.height = function(value) {
        if (!arguments.length) {
            return height;
        }
        height = value;
        return chart;
    };


    // chart.columnForColors = function(value) {
    //     if (!arguments.columnForColors) {
    //         return columnForColors;
    //     }
    //     columnForColors = value;
    //     return chart;
    // };

    // chart.columnForRadius = function(value) {
    //     if (!arguments.columnForRadius) {
    //         return columnForRadius;
    //     }
    //     columnForRadius = value;
    //     return chart;
    // };

    return chart;
}