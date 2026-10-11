// Content for the site. Facts come from Arsenal's own pages and press releases
// (2023–2025); anything time-sensitive should be re-checked before launch.
window.ARSENAL = {
  // Each vertical is also a star in the hero constellation. x/y are positions
  // inside the constellation's box (0..1). state: "foundation" | "building" | "next".
  verticals: [
    { id: "platform", name: "Shared AI Platform", short: "Core", state: "core", x: 0.50, y: 0.06,
      line: "The models, data and agents every company runs on.",
      body: "One platform underneath the whole portfolio. Each company inherits the tooling, data pipelines and agentic services the others built.",
      tags: ["AI", "Agentic services", "Shared"] },
    { id: "energy", name: "Energy", short: "Foundation", state: "foundation", x: 0.31, y: 0.50,
      line: "Production, infrastructure and waste-to-energy, generating cash flow today.",
      body: "Anchored by Blackrock Midstream, a natural gas processing and infrastructure company acquired in March 2023. Operations span upstream, midstream and downstream, plus biogas waste-to-energy.",
      tags: ["Blackrock Midstream", "Natural gas", "Biogas"] },
    { id: "finance", name: "Finance", short: "Foundation", state: "foundation", x: 0.13, y: 0.94,
      line: "Specialized financing and M&A for energy service companies.",
      body: "Financing and merger & acquisition services for oil and gas service companies across North America’s main basins. AI-driven underwriting cuts credit decisions from weeks to days.",
      tags: ["Lending", "M&A", "Underwriting"] },
    { id: "accounting", name: "Accounting AI", short: "Building", state: "building", x: 0.69, y: 0.50,
      line: "AI-native accounting, built for the firms that do the work.",
      body: "An AI-native accounting company built on the shared platform, putting agentic workflows into the practice.",
      tags: ["AI-native", "Agentic"] },
    { id: "insurance", name: "Insurance", short: "Building", state: "building", x: 0.87, y: 0.94,
      line: "Insurance products with AI in the loop.",
      body: "A vertical insurance business where AI handles the repetitive work and people handle the judgment.",
      tags: ["AI-native", "Vertical"] },
    { id: "mfo", name: "Multi-Family Office", short: "Building", state: "building", x: 0.50, y: 0.66,
      line: "Wealth, tax and succession strategy for high-net-worth families.",
      body: "Tax, succession and capital strategies for high-net-worth clients, delivered with the same AI tooling as the rest of the portfolio.",
      tags: ["Wealth", "Tax", "Succession"] },
    { id: "twins", name: "Digital Twins", short: "Building", state: "building", x: 0.50, y: 0.34,
      line: "Live digital models of physical operations.",
      body: "Digital twins of physical assets, starting with the energy operations Arsenal already runs.",
      tags: ["Simulation", "Operations"] },
    { id: "health", name: "Healthcare", short: "Next", state: "next", x: 1.04, y: 0.30,
      line: "The next vertical to light up.",
      body: "Healthcare is the next vertical on the chart, to be built on the same platform and operating model.",
      tags: ["Next"] }
  ],
  // Constellation edges by id. dashed = not yet built.
  edges: [
    ["platform", "twins"], ["platform", "energy"], ["platform", "accounting"],
    ["energy", "finance"], ["accounting", "insurance"],
    ["energy", "mfo"], ["mfo", "accounting"], ["twins", "mfo"],
    ["accounting", "health", "dashed"]
  ],
  record: [
    { when: "2003", title: "Incorporated", text: "The company that becomes Arsenal is incorporated as Global Green Solutions Inc." },
    { when: "2022", title: "Renamed Arsenal", text: "Name and symbol change to Arsenal Digital Holdings, Inc., trading as ADHI." },
    { when: "Mar 2023", title: "Blackrock Midstream", text: "Acquires the natural gas processing and infrastructure company, establishing the energy foundation." },
    { when: "Aug 2023", title: "First revenues", text: "Reports its first revenues and advances operations." },
    { when: "Mar 2024", title: "Expansion", text: "Announces a plan to build a processing plant in South Texas, following Blackrock Midstream’s revenue performance." },
    { when: "Jun 2025", title: "New command", text: "Appoints a new CEO, President and CMO, names a new Board Chairman and expands the board." },
    { when: "Jul 2025", title: "Uplisting path", text: "Announces a strategic business plan and engages securities counsel and an accounting firm ahead of uplisting." },
    { when: "Oct 2025", title: "Victoria, Texas", text: "Identifies a site near Victoria, Texas with terminal, railcar and barge access." },
    { when: "Dec 2025", title: "Registration", text: "Reports SEC registration progress. Mandel Innovation Fund commits to a convertible note as lead institutional investor." }
  ],
  roster: [
    { name: "Todd A. Bass", role: "Chief Executive Officer" },
    { name: "Russell Houle", role: "President" },
    { name: "Ryan Messer", role: "Chief Operating Officer · Executive Director" },
    { name: "Ian Lahde", role: "Chief Marketing Officer" },
    { name: "Jordan Mandel", role: "Chairman of the Board" },
    { name: "Charles Holloway", role: "Director" },
    { name: "Randall Eddington", role: "Founder, Blackrock Midstream" }
  ]
};
