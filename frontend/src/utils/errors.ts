import axios from 'axios';

export function getErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;

    if (typeof detail === 'string') {
      return detail;
    }

    if (Array.isArray(detail) && detail.length > 0) {
      return detail
        .map((item) => item?.msg)
        .filter(Boolean)
        .join(' ');
    }

    if (typeof error.response?.data?.message === 'string') {
      return error.response.data.message;
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'Something went wrong.';
}
