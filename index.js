const express = require("express");
const path = require("path");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, "public")));

let arr=[]
let playingArray=[]

io.on("connection",(socket)=>{
    socket.on("find",(e)=>{

        if(e.name!=null){

            arr.push(e.name)

            if(arr.length>=2){
                let p1obj1={
                    p1name:arr[0],
                    p1value:"x",
                    p1move:""
                }
                  if(arr.length>=2){
                let p1obj1={
                    p1name:arr[0],
                    p1value:"x",
                    p1move:""
            }

            let obj= {
                p1: p1obj,
                p2: p2obj

            }
            playingArray.push(obj)

            arr.splice(0,2)

                  }
                  }
        }

    })
})

// Send 'index.html' for the root route
app.get("/", (req, res) => {
    return res.sendFile(path.join(__dirname, "public", "index.html"));
});

server.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});
