import userModel from "../models/userModel.js";
import bcrypt from "bcryptjs";
import asyncHandler from "express-async-handler";
import jwt from "jsonwebtoken";
import { v2 as cloudinary } from "cloudinary";
import { CloudinaryStorage } from "multer-storage-cloudinary";
import multer from "multer";
import imageModel from "../models/imageModel.js";

// Configure Cloudinary
cloudinary.config({
  cloud_name: "dwkuxikyi",
  api_key: "148237439839667",
  api_secret: "8IN_RaZVPEKfslXXEKWjHRX1xWw",
});

// Configure multer to use Cloudinary as storage
const storage = new CloudinaryStorage({
  cloudinary: cloudinary,
  params: {
    folder: "air canvas",
    format: async (req, file) => "png", // supports promises as well
    public_id: (req, file) => "image-" + Date.now(), // use your own public_id here
  },
});
const parser = multer({ storage: storage });

const registerController = asyncHandler(async (req, res) => {
  const { name, password, email, phone } = req.body;
  if (!name || !password || !email || !phone) {
    return res
      .status(400)
      .json({ message: "Provide complete data", success: false });
  }
  if (phone.length !== 10)
    return res.status(400).json({
      message: "Phone number should be of 10 numbers",
      success: false,
    });
  const registeredUser = await userModel.findOne({
    $or: [{ email: email }, { phone: phone }],
  });
  if (registeredUser) {
    return res.status(400).json({
      message: `User is already registered with email ${email}`,
      success: false,
    });
  }
  const salt = await bcrypt.genSalt(10);
  const hashedPassword = await bcrypt.hash(password, salt);
  const user = new userModel({
    name,
    email,
    phone,
    password: hashedPassword,
  });
  const result = await user.save();
  if (result) {
    return res.status(200).json({
      message: `User is registered successfully.`,
      data: result,
      success: true,
    });
  }
});
const loginController = asyncHandler(async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res
      .status(400)
      .json({ message: "Provide complete data", success: false });
  }
  const user = await userModel.findOne({ email: email });
  if (!user) {
    return res.status(400).json({ message: "user not found.", success: false });
  }
  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch) {
    return res
      .status(400)
      .json({ message: "Invalid Email and password", success: false });
  }
  const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, {
    expiresIn: "1d",
  });
  return res.status(200).json({
    message: "Login Success",
    success: true,
    token,
    name: user.name,
    userID: user._id,
  });
});

const authController = asyncHandler(async (req, res) => {
  const user = await userModel.findById(req.body.userID);
  if (!user) {
    return res.status(404).json({
      message: "User not found.",
      success: false,
    });
  } else {
    return res.status(200).json({
      success: true,
      data: {
        name: user.name,
        email: user.email,
        id: user.id,
      },
    });
  }
});

const userProfileUpdateController = asyncHandler(async (req, res) => {
  const { userID } = req.params;
  if (!userID)
    return res
      .status(400)
      .json({ message: "Provide complete data", success: false });
  let { name, email, phone } = req.body;
  const user = await userModel.findById(userID);
  if (!user)
    return res.status(400).json({ message: "No user found", success: false });
  if (!name) name = user.name;
  if (!email) email = user.email;
  if (!phone) phone = user.phone;
  const result = await userModel.findByIdAndUpdate(
    user._id,
    {
      name,
      email,
      phone,
    },
    { new: true }
  );
  if (result)
    return res.status(200).json({
      message: "Profile updated successfully",
      data: result,
      success: true,
    });
});

const imageSender = asyncHandler(async (req, res) => {
  const userID = req.body.userID;
  if (!userID)
    return res.status(400).json({ message: "Error no user id found" });
  const img = await imageModel.find({ user: userID });
  if (img.length === 0)
    return res.status(200).json({ message: "No images drawn" });
  return res.status(200).json({ imageURL: img });
});

const userImageUploader = asyncHandler(async (req, res) => {
  // const { img } = req.body.files;

  parser.single("img")(req, res, async (err) => {
    if (err) {
      return res.status(400).json({ error: err.message });
    }
    const userID = req.body.userID;
    const user = await userModel.findById(req.body.userID);
    if (!user) return res.status(400).json({ message: "user doesn't exists" });
    const image = new imageModel({
      url: req.file.path,
      user: userID,
    });
    const result = await image.save();
    if (result) {
      return res.status(200).json({ imageUrl: req.file.path });
    }
  });
});

const deleteImage = asyncHandler(async (req, res) => {
  const imageID = req.body.imageID;
  if (!imageID)
    return res.status(400).json({ message: "Image Id is not given" });
  const result = await imageModel.findByIdAndDelete(imageID);
  if (!result) return res.status(400).json({ message: "No such image exists" });
  return res.status(200).json({ message: "Image deleted successfully" });
});

export {
  loginController,
  registerController,
  authController,
  userProfileUpdateController,
  userImageUploader,
  imageSender,
  deleteImage,
};
