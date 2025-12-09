from pydantic_settings import BaseSettings
from pydantic import BaseModel


class SupbaseSettings(BaseModel):
    url: str = "https://hdcaauixnflpnytisrbu.supabase.co"
    anon_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhkY2FhdWl4bmZscG55dGlzcmJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE0MDIyNDAsImV4cCI6MjA3Njk3ODI0MH0.VqBtP1qlp6nA3DEum_1YN7Qg5bCsoJKSKU4eU7K_01s"
    service_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhkY2FhdWl4bmZscG55dGlzcmJ1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTQwMjI0MCwiZXhwIjoyMDc2OTc4MjQwfQ.yT37xHd95W0tguFzFz-mD32D6redAQxgS8MuVF9Bru0"


class Settings(BaseSettings):
    supabase: SupbaseSettings = SupbaseSettings()
    postgres_connection_string: str = "postgresql://postgres.hdcaauixnflpnytisrbu:SupabasePassword123!@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres"


settings = Settings()
