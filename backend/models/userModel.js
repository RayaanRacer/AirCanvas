import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
    name:{
        type:String,
        required:[true,'name is required']
    },
    email:{
        type:String,
        required:[true,'email is required']
    },
    phone:{
        type:Number,
        required:[true,'phone is required']
    },
    password:{
        type:String,
        required:[true, 'password is required']
    }
})

const userModel = mongoose.model('users',userSchema)

export default userModel;