export function getCsrfToken(): string {
  // Retrieve the CSRF token from the cookies
  const csrfToken: string | undefined = document.cookie
    .split("; ")
    .find((row: string) => row.startsWith("csrftoken="))
    ?.split("=")[1];

  // If no CSRF token is found, log an error and return an empty string
  if (!csrfToken) {
    console.error("CSRF token not found.");
    return "";
  }

  return csrfToken;
}
