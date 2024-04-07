import express from "express";
import {
  deleteImage,
  imageSender,
  // authController,
  loginController,
  registerController,
  userImageUploader,
  userProfileUpdateController,
} from "../controllers/userController.js";
// import { isUser } from "../middleware/authMiddleware.js";
// import { getAllDoctors } from "../controllers/doctorController.js";
// import {
//   getAppointmentByUser,
//   getUniqueAppointmentByUser,
// } from "../controllers/appointmentController.js";

// router onject
const router = express.Router();

// routes

router.post("/login", loginController);
router.post("/register", registerController);
router.post("/uploadImage", userImageUploader);
router.get("/sendImage", imageSender);
// router.post("/getUserData", isUser, authController);
// router.get("/getAllDoctors", getAllDoctors);
// router.get("/getAllAppointments/:userID", getAppointmentByUser);
router.put("/updateUserProfile", userProfileUpdateController);
router.get("/deleteImage", deleteImage);
// router.get("/getUniqueAppointments/:userID", getUniqueAppointmentByUser);

export default router;
