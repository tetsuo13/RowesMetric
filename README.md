# Analysis of Noticeability and Suspiciousness in Rowe's Exposure Metric

Video surveillance is an increasingly open problem in the security field where
we would like "suspicious" behavior to be distinguished. Using Rowe's exposure
metric, agents in a sensor field can be ranked for deceptiveness based on
several measurements. Noticeability and suspiciousness are two of the most
important metrics in measuring the exposure of a deceptive agent. Our research
analyses the effectiveness of these two metrics using statistical techniques
and simulated datasets. In this paper our results and findings will be
discussed in detail.

Undergraduate research project at UNCG. Mentored by
[Dr. Shan Suthaharan](http://www.uncg.edu/cmp/faculty/s_suthah/) as part of
CSC 593 (Directed Study in Computer Science).

## Agent Positional Data Format

Agent positional data is saved in JSON format. This was chosen due to its
nonverbosity when compared to XML and other formats since the Kinect motion
sensor records at 30 fps.

The data file, saved under the name ```data.json``` by default in the same
directory as the Kinect - Agent Capture application, can be used against
multiple recording sessions. Each newly added agent is assigned a unique ID.
The entire data set is stored under the "agents" array, with each agent
represented as an object within the array. Each agent contains the following
three keys:

- **deceptive**: Boolean to denote whether the agent is a known deceptive agent.
- **positions**: Array containing the recorded positional data. Each array
                 contains two elements representing the X and Y position
                 relative to the Kinect sensor. (This is the X and Z axis
                 information from the Kinect API.)
- **agentid**: Unique identifier for the agent. For each new agent added to the
               ```agents``` array, this ID is the previously recorded highest
               ID plus one.

Example of a ```data.json``` file with one agent:

```json
{
  "agents": [
    {
      "deceptive": false,
      "positions": [
        [0.442923,3.37065864],
        [0.441173434,3.37511969]
      ],
      "agentid": 1
    }
  ]
}
```

All subprojects which process the data file in any way expect it to be in this
format.

## Subprojects

### Kinect - Agent Capture

Application which uses motion capture to records agent positions. Recorded data
is then saved to disk using the interproject data format.

#### Requirements

* Kinect SDK 1.5.0

### Presentation

Presentation used at [The Eighth Annual Regional Mathematics and Statistics
Conference](http://www.uncg.edu/mat/rmsc/) at UNCG on November 3rd, 2012.

Utilizes [reveal.js](https://github.com/hakimel/reveal.js).

### Metric

#### Requirements

* Python 2.7
* matplotlib (optional, used only for plotting agent data)

### Paper

#### Requirements

* LaTeX