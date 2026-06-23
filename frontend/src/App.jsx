import { useState } from "react";
import axios from "axios";
import Login from "./pages/login";
import Signup from "./pages/sign";
import Dashboard from "./pages/dashboard";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Friends from "./pages/friends";
import ProtectedAPI from "./pages/protectedapi";

function App() {
  // const [loading, setLoading] = useState(false);
  // const [location, setLocation] = useState(null);

  // const sendSOS = () => {
  //   setLoading(true);

  //   navigator.geolocation.getCurrentPosition(
  //     async (position) => {
  //       const lat = position.coords.latitude;
  //       const lng = position.coords.longitude;

  //       setLocation({ lat, lng });

  //       try {
  //         const { data } = await axios.post(
  //           "https://crispy-space-acorn-jj59jvrp5wxqhp69r-8000.app.github.dev/send_mail",
  //           {
  //             lat,
  //             lng,
  //           }
  //         );

  //         alert("SOS Alert Sent!");
  //         console.log(data);
  //       } catch (error) {
  //         console.error(error);
  //         alert("Failed to send SOS");
  //       }

  //       setLoading(false);
  //     },
  //     (error) => {
  //       console.error(error);
  //       alert("Location permission denied");
  //       setLoading(false);
  //     }
  //   );
  // };

  // return (
  //   <div
  //     style={{
  //       height: "100vh",
  //       display: "flex",
  //       flexDirection: "column",
  //       justifyContent: "center",
  //       alignItems: "center",
  //     }}
  //   >
  //     <h1>Aegis SOS</h1>

  //     {location && (
  //       <p>
  //         Lat: {location.lat}
  //         <br />
  //         Lng: {location.lng}
  //       </p>
  //     )}

  //     <button
  //       onClick={sendSOS}
  //       disabled={loading}
  //       style={{
  //         width: "200px",
  //         height: "200px",
  //         borderRadius: "50%",
  //         border: "none",
  //         fontSize: "24px",
  //         cursor: "pointer",
  //       }}
  //     >
  //       {loading ? "Sending..." : "SOS"}
  //     </button>
  //   </div>
  // );

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Signup />} />
          <Route path="/dashboard" element={<ProtectedAPI><Dashboard /></ProtectedAPI>} />
          <Route path="/friends" element={<ProtectedAPI><Friends /></ProtectedAPI>} />

        </Routes>
      </Router>
     
    </div>
  )
}

export default App;