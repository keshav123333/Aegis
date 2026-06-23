import { useEffect, useRef, useState } from "react";
import Sidebar from "./sidebar";

export default function Dashboard() {
  const [sharing, setSharing] = useState(false);
  const [locations, setLocations] = useState({});
  const [msg, setMsg] = useState("location");
  
  
 

  const wsRef = useRef(null);
  const watchIdRef = useRef(null);

useEffect(() => {

  const token = localStorage.getItem("token");

  const ws = new WebSocket(
    `wss://crispy-space-acorn-jj59jvrp5wxqhp69r-8000.app.github.dev/ws/location?token=${token}`
  );

  wsRef.current = ws;
   ws.onopen = () => {
    console.log("Connected");
  };

  ws.onmessage = (event) => {
    

    const data = JSON.parse(event.data);
    console.log("Received:", data);

    switch (data.type) {

      case "sos_alert"  :

        console.log(
          "SOS from",
          data.user_id
        );
        alert(`SOS Alert from User ${data.user_id}! Location: (${data.lat}, ${data.lng})`);

        setLocations(prev => ({
          ...prev,
          [data.user_id]: {
            lat: data.lat,
            lng: data.lng
          }
        }));

        break;

      case "sos_update":
        
        console.log(
          "SOS update from",
          data.user_id
        );
        setLocations(prev => (
          {...prev,
          [data.user_id]: {
            lat: data.lat,
            lng: data.lng
          }
        }
        ) )

        break;
      case "location_update":

        console.log(
          "Location update"
        );

        break;
    }
  };
 ws.onclose = () => {
    console.log("Disconnected");
  };
  return () => ws.close();

}, []);




useEffect(() => {

  watchIdRef.current =
    navigator.geolocation.watchPosition(
      (position) => {
        console.log(msg)
        if (
          wsRef.current?.readyState ===
          WebSocket.OPEN
        ) {

          wsRef.current.send(
            JSON.stringify({
              type: msg,
              lat: position.coords.latitude,
              lng: position.coords.longitude
            })
          );

        }
      }
    );

  return () =>
    navigator.geolocation.clearWatch(
      watchIdRef.current
    );

}, [msg]);

  const startSharing = () => {
    
    


   

    

   
     navigator.geolocation.getCurrentPosition(
    (position) => {
 if (
          wsRef.current?.readyState ===
          WebSocket.OPEN
        ) {
      wsRef.current.send(
        JSON.stringify({
          type: "sos_alert",
          lat: position.coords.latitude,
          lng: position.coords.longitude
        })
      );
    }
        setMsg("sos_update");
        setSharing(true);

    }
  

  );

 

  
     
 

};

  const stopSharing = () => {
     setMsg("location");
     setSharing(false);
    }
 


  return (

    <div className="container">
      <Sidebar />
     
     
<div className="content">



      {sharing ? (
        <button onClick={stopSharing}>
          Stop Sharing
        </button>
      ) : (
        <button onClick={startSharing}>
          Start Sharing
        </button>
      )}

 <div>
      <h2>Friend Locations</h2>

      {Object.entries(locations).map(
        ([userId, location]) => (
          <div key={userId}>
            <strong>User {userId}</strong>

            <p>Lat: {location.lat}</p>
            <p>Lng: {location.lng}</p>
            <a href={`https://www.google.com/maps?q=${location.lat},${location.lng}`} target="_blank" rel="noopener noreferrer">
              View on Map
            </a>
          </div>
        )
      )}
    </div>


</div>




    </div>
  );
}