import {useState,useRef} from "react";
import axios from "axios";

function Friends(){
const [friends, setFriends] = useState([]);
const [friendUsername, setFriendUsername] = useState("");
const addref=useRef(null)

const handleAddFriend = async () => {
    if(friendUsername.trim() === "") {
        alert("Please enter a username");
        return;
    }

    try{
        
         setFriends((prev)=>([...prev,friendUsername]))
    }
    catch(err){
        console.error(err);
        alert("Failed to add friend");
    }

        // Send request to backend to add friend
}

// const delete_friends=(index)=>{
//     setFriends(prev=>prev.filter((_,i)=>i!==index))
// }
    return (
        <div>
            <h1>Friends Page</h1>
            <input type="text" 
                   value={friendUsername}
                   onChange={(e) => setFriendUsername(e.target.value)}
                   placeholder="Add friend by username" />
            <button onClick={handleAddFriend} ref={addref}>Add Friend</button>

        
            {friends.length > 0 && friends.map((frnd,index)=>(
                <li key={index}>{frnd} </li>
            ))}
           

        </div>
    )
}

export default Friends