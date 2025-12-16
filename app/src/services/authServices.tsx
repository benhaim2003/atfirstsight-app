import { User } from "@/src/types/user";

export default function signIn(email: string, password: string): User {
    console.log("Sign in with email:", email, "password:", password)
    
    const user: User = {
        id: Math.random().toString(36).substring(7),
        email,
        created_at: new Date()
    };

    return user
}