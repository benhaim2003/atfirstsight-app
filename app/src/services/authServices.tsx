import { User } from "@/src/types/user";

export function logIn(email: string, password: string): User | null {
    console.log("Log In with email:", email, "password:", password)
    // Get user from server

    // return user or null if not exist
    return null
}

export function signUp(email: string, password: string): User {
    console.log("Sign Up with email:", email, "password:", password)
    
    const user: User = {
        id: Math.random().toString(36).substring(7),
        email,
        created_at: new Date()
    };

    return user
}