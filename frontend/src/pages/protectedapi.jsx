import { useNavigate } from "react-router-dom";
function ProtectedAPI({children}) {
  const navigate = useNavigate();

  const token=localStorage.getItem('token')

return token? children : navigate('/login');
}
export default ProtectedAPI;
