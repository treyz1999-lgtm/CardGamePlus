import { useCallback, useState } from 'react';
import { getErrorMessage } from '../utils/errors';

export function useAsyncAction<TArgs extends unknown[]>(
  action: (...args: TArgs) => Promise<void>,
) {
  const [isWorking, setIsWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = useCallback(
    async (...args: TArgs) => {
      setIsWorking(true);
      setError(null);

      try {
        await action(...args);
      } catch (caughtError) {
        setError(getErrorMessage(caughtError));
      } finally {
        setIsWorking(false);
      }
    },
    [action],
  );

  return { run, isWorking, error, setError };
}
