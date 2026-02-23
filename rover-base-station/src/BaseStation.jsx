import { useState } from "react";
import Home from "./home.jsx";
import Delivery from "./Delivery.jsx";
import Equipment from "./Equipment.jsx";
import Autonomous from "./Autonomous.jsx";
import Science from "./Science.jsx";
import "./BaseStation.css";
function BaseStation() {
  const [activeTab, setActiveTab] = useState("home");
  return (
    <div>
    {/*changes the screen depending on button clicks*/}
    <div className="button-bar">
    <button className= "tab-button" onClick={() => setActiveTab("home")}>Home</button>
    <button className= "tab-button" onClick={() => setActiveTab("delivery")}>Delivery Mission</button>
    <button className= "tab-button" onClick={() => setActiveTab("equipment")}>Equipment Servicing Mission</button>
    <button className= "tab-button" onClick={() => setActiveTab("autonomous")}>Autonomous Navigation Mission</button>
    <button className= "tab-button" onClick={() => setActiveTab("science")}>Science Mission</button>
    </div>
    
    {/* if the tab changes, change the component on screen*/}
    {activeTab === "home" && <Home />}
    {activeTab === "delivery" && <Delivery />}
    {activeTab === "equipment" && <Equipment />}
    {activeTab === "autonomous" && <Autonomous />}
    {activeTab === "science" && <Science />}
  
    </div>
  )
}

export default BaseStation
