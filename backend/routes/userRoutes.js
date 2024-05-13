import express from "express";
import {
  checkStatus,
  createRazorpayOrder,
  deleteImage,
  imageSender,
  // authController,
  loginController,
  registerController,
  userApprove,
  userImageUploader,
  userProfileUpdateController,
  verifySignature,
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
router.post("/create-order", createRazorpayOrder);
router.post("/verify-order", verifySignature);
router.post("/check-status", checkStatus);
router.post("/user-approve", userApprove);
// router.get("/getUniqueAppointments/:userID", getUniqueAppointmentByUser);

export default router;
