export function ErrorMessage({ message }: { message: string }) {
  return (
    <div className="error-message" role="alert">
      <strong>Something went wrong:</strong> {message}
    </div>
  );
}
