import axios from "axios";
import { User } from "@/src/types/user";

const API_BASE_URL = "http://192.168.2.104:8080";


export async function logIn(email: string, password: string): Promise<User | null> {
    try {
        const response = await axios.post(`${API_BASE_URL}/users/signin`, {
            email,
            password
        });
        
        const { id, email: userEmail } = response.data;
        
        console.log("LOGIN to ", email)

        const user: User = {
            id,
            email: userEmail,
            created_at: new Date()
        };
        
        return user;
    } 
    catch (error) {
        console.error("Sign in failed:", error);
        return null;
    }
}

export async function signUp(email: string, password: string): Promise<User | null> {
    try {
        const response = await axios.post(`${API_BASE_URL}/users/signup`, {
            email,
            password
        });
        
        const { id, email: userEmail } = response.data;
        
        console.log("SIGNUP for ", email)

        const user: User = {
            id,
            email: userEmail,
            created_at: new Date()
        };
        
        return user;
    } 
    catch (error) {
        console.error("Sign up failed:", error);
        return null;
    }
}