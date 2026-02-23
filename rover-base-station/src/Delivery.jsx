import "./BaseStation.css";
import { useState, useEffect } from "react";
export default function Delivery() {
  return (
    <div className="container"> 
    <h1 className="title"> Delivery Mission </h1>
    </div>
  );
}

function Timer()
{
    const [seconds, setSeconds] = useState(0);
    useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(prev => prev + 1); // increment every second
    }, 1000);

    return () => clearInterval(interval); // cleanup when component unmounts
  }, []); // empty array = run once on mount

  return <h1>Seconds: {seconds}</h1>;
}

