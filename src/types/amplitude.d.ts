interface Window {
  amplitude: {
    add: (plugin: any) => void;
    init: (apiKey: string, config?: Record<string, unknown>) => void;
  };
  sessionReplay: {
    plugin: (options: { sampleRate: number }) => any;
  };
}
