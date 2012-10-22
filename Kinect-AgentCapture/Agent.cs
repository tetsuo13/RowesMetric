using Newtonsoft.Json;
using System.Collections.Generic;

namespace UNC.Greensboro.CSC.FiveNineThree.anicholson
{
    public class Agent
    {
        public bool deceptive { get; set; }
        public List<float[]> positions { get; set; }

        [JsonProperty(PropertyName = "agentid")]
        public uint agentId { get; set; }

        public Agent()
        {
            this.positions = new List<float[]>();
            this.agentId = 0;
        }
    }
}
