import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>My App</h2>

      <ul>
        <li><Link to="/">Dashboard</Link></li>
        <li><Link to="/profile">Profile</Link></li>
        <li><Link to="/friends">Friends</Link></li>
        <li><Link to="/settings">Settings</Link></li>
      </ul>
    </div>
  );
}
export default Sidebar